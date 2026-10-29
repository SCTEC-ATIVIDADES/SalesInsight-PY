---

description: "Task list for RF01 – Criar ou Carregar o Dataset de Vendas implementation"
---

# Tasks: RF01 – Criar ou Carregar o Dataset de Vendas

**Input**: Design documents from `/specs/001-sales-dataset-generator/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Included as REQUIRED by Constitution Principle III (Desenvolvimento Orientado a Testes - TDD INEGOCIÁVEL). All test tasks MUST be written first and fail before implementation.

**Organization**: Tasks are grouped by user story (`US1`, `US2`, `US3`) to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Root modules**: `gerador_dados.py` (geração independente do dataset), `modulo_vendas.py` (leitura/processamento do pipeline), `main.py`, `vendas.csv`, `requirements.txt` at repository root
- **Tests**: `tests/test_modulo_vendas.py`
- **Container & Docs**: `Dockerfile`, `docker-compose.yml`, `README.md`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, dependency pinning, and directory structure per `plan.md` and Constitution Principle V.

- [ ] T001 Create `requirements.txt` at repository root with pinned versions for `pandas`, `pytest`, and `Faker`
- [ ] T002 [P] Create `tests/` directory and initialize `tests/test_modulo_vendas.py` with pytest imports and module import scaffold
- [ ] T003 [P] Create `Dockerfile` and configure `docker-compose.yml` at repository root to run `python main.py` and `pytest` mounting project root volume

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Domain catalog constants and module skeleton in `gerador_dados.py` and `modulo_vendas.py` that all user stories depend on.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [ ] T004 Define domain catalog constants (`CABECALHO_VENDAS`, `PRODUTOS`, `CATEGORIAS`, `REGIOES`) in `gerador_dados.py` (and import in `modulo_vendas.py`) matching `data-model.md` constraints (`["id_venda", "data_venda", "cliente", "produto", "categoria", "regiao", "quantidade", "preco_unitario"]`, products `["Notebook", "Smartphone", "Tablet", "Monitor", "Teclado", "Mouse"]`, categories `{"Notebook": "Eletrônicos", "Monitor": "Eletrônicos", "Smartphone": "Celulares", "Tablet": "Celulares", "Teclado": "Acessórios", "Mouse": "Acessórios"}`, regions `["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]`)

**Checkpoint**: Foundation ready - user story implementation can now begin in priority order (or in parallel).

---

## Phase 3: User Story 1 - Geração Automatizada de Dataset de Vendas Realista (Priority: P1) 🎯 MVP

**Goal**: Gerar de forma determinística o arquivo `vendas.csv` com no mínimo 100 registros realistas (usando `Faker('pt_BR')` e `random` com `seed=42`), 8 colunas obrigatórias e inconsistências deliberadas controladas (~5% `quantidade` vazia, ~5% `preco_unitario` vazio, ~10% `produto` com espaços sobressalentes `f"  {prod} "`, e duplicata `dados[0]`).

**Independent Test**: Executar `pytest tests/test_modulo_vendas.py -k "gerar_dataset"` e verificar que `gerar_dataset_sintetico(tmp_path / "vendas.csv", n_registros=100, seed=42)` cria um arquivo CSV UTF-8 com cabeçalho exato de 8 colunas, 101 linhas de dados (100 + 1 duplicata), ruídos esperados e reprodutibilidade idêntica para a mesma `seed`.

### Tests for User Story 1 (TDD - Red Phase) ⚠️

> **NOTE: Write these tests FIRST in `tests/test_modulo_vendas.py`, ensure they FAIL before implementing `gerar_dataset_sintetico`**

- [ ] T005 [P] [US1] Write unit test `test_gerar_dataset_sintetico_cria_arquivo_e_cabecalho` in `tests/test_modulo_vendas.py` verifying file creation, UTF-8 encoding, exact 8-column header (`["id_venda", "data_venda", "cliente", "produto", "categoria", "regiao", "quantidade", "preco_unitario"]`), and minimum 100 records (`n_registros=100` producing 101 rows with duplicate `dados[0]`)
- [ ] T006 [P] [US1] Write unit test `test_gerar_dataset_sintetico_determinismo_seed` in `tests/test_modulo_vendas.py` verifying two calls with `seed=42` produce byte-identical CSV files and invalid `n_registros < 1` raises `ValueError`
- [ ] T007 [P] [US1] Write unit test `test_gerar_dataset_sintetico_inconsistencias_deliberadas` in `tests/test_modulo_vendas.py` verifying presence of empty `quantidade` (`""`), empty `preco_unitario` (`""`), padded whitespace in `produto` (`f"  {prod} "`), duplicate first record (`dados[0]`), valid ISO dates `2024-MM-DD`, quantity range `"1"` to `"8"`, and unit price range `"100.0"` to `"3500.0"`

### Implementation for User Story 1 (TDD - Green & Refactor Phase)

- [ ] T008 [US1] Implement `gerar_dataset_sintetico(caminho_arquivo="vendas.csv", n_registros=100, seed=42) -> str` in `gerador_dados.py` (and re-export in `modulo_vendas.py`) using `Faker('pt_BR')` (`seed_instance(seed)`), `random.Random(seed)`, and `csv.writer` (`encoding="utf-8"`, `newline=""`), enforcing constraints: sequential `id_venda` (`1..n_registros`), `data_venda` in `2024` (`YYYY-MM-DD`), 30-client pool in `cliente`, ~10% `f"  {prod} "` padding in `produto`, ~5% `""` in `quantidade` (otherwise `randint(1, 8)`), ~5% `""` in `preco_unitario` (otherwise `round(uniform(100, 3500), 2)`), writing `dados[0]` duplicate row before `writer.writerows(dados)`, and printing `[OK] Dataset gerado em: {caminho_arquivo}`

**Checkpoint**: At this point, User Story 1 (`gerar_dataset_sintetico`) is fully functional and passes all US1 unit tests independently.

---

## Phase 4: User Story 2 - Carregamento Estruturado de Dataset CSV Existente (Priority: P2)

**Goal**: Carregar qualquer arquivo CSV de vendas compatível utilizando `csv.DictReader` em `carregar_csv(caminho_arquivo="vendas.csv")`, retornando `list[dict[str, str]]` com chaves correspondentes ao cabeçalho e preservando fielmente valores brutos (incluindo strings vazias e espaços extras).

**Independent Test**: Executar `pytest tests/test_modulo_vendas.py -k "carregar_csv"` e verificar que um CSV existente é convertido em `list[dict[str, str]]` preservando todas as linhas, chaves de cabeçalho e valores brutos sem sobrescrever o arquivo existente.

### Tests for User Story 2 (TDD - Red Phase) ⚠️

- [ ] T009 [P] [US2] Write unit test `test_carregar_csv_retorna_lista_dicionarios_preservando_brutos` in `tests/test_modulo_vendas.py` verifying `carregar_csv` reads CSV via `csv.DictReader` into `list[dict[str, str]]` preserving raw strings (`""` and `"  Notebook "`) and exact 8 keys

### Implementation for User Story 2 (TDD - Green & Refactor Phase)

- [ ] T010 [US2] Implement `carregar_csv(caminho_arquivo="vendas.csv") -> list[dict[str, str]]` in `modulo_vendas.py` using `csv.DictReader` (`mode="r"`, `encoding="utf-8"`, `newline=""`) and explicit `for` loop to build and return `list[dict[str, str]]`
- [ ] T011 [US2] Implement RF01 orchestration entry point in `main.py` importing `gerar_dataset_sintetico` from `gerador_dados` and `carregar_csv` from `modulo_vendas`, checking `if not os.path.exists(arquivo_dados): gerar_dataset_sintetico(arquivo_dados, n_registros=150)` followed by `dados_brutos = mv.carregar_csv(arquivo_dados)` without overwriting existing `vendas.csv`

**Checkpoint**: At this point, User Stories 1 AND 2 both work independently and through `main.py`.

---

## Phase 5: User Story 3 - Parametrização de Caminhos e Tratamento Seguro de Arquivos Ausentes (Priority: P3)

**Goal**: Garantir ausência de caminhos fixos (hardcoded), criação automática de diretórios pais em `gerar_dataset_sintetico` e tratamento resiliente de `FileNotFoundError`/`OSError` em `carregar_csv` (retornando `[]` e exibindo mensagem clara sem interromper a execução com traceback não tratado).

**Independent Test**: Executar `pytest tests/test_modulo_vendas.py -k "inexistente or subdiretorio"` e verificar que `carregar_csv("nao_existe.csv")` retorna `[]` com mensagem `[ERRO]` no stdout e `gerar_dataset_sintetico(tmp_path / "subdir/vendas.csv")` cria o diretório pai automaticamente.

### Tests for User Story 3 (TDD - Red Phase) ⚠️

- [ ] T012 [P] [US3] Write unit tests `test_carregar_csv_arquivo_inexistente_retorna_lista_vazia` and `test_gerar_dataset_cria_diretorio_pai_automaticamente` in `tests/test_modulo_vendas.py` verifying resilient `[]` return + error message on missing file and parent directory creation for nested paths

### Implementation for User Story 3 (TDD - Green & Refactor Phase)

- [ ] T013 [US3] Add parent directory creation (`Path(caminho_arquivo).parent.mkdir(parents=True, exist_ok=True)`) in `gerar_dataset_sintetico` (`gerador_dados.py`) and `try...except (FileNotFoundError, OSError)` error handling in `carregar_csv` (`modulo_vendas.py`) printing `[ERRO] Arquivo não encontrado: {caminho_arquivo}` and returning `[]`

**Checkpoint**: All user stories (US1, US2, US3) are independently functional and tested.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final dataset generation, documentation, and end-to-end validation per `quickstart.md` and Constitution Quality Gates.

- [ ] T014 Generate default `vendas.csv` at repository root using `gerar_dataset_sintetico("vendas.csv", n_registros=150, seed=42)` and verify `python main.py` and `pytest` pass with 100% green suite
- [ ] T015 [P] Update `README.md` at repository root documenting RF01 dataset structure, justification for `csv.DictReader` + `Faker('pt_BR')`, TDD workflow, and execution commands from `specs/001-sales-dataset-generator/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1: T001–T003)**: No dependencies - can start immediately
- **Foundational (Phase 2: T004)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3: T005–T008)**: Depends on T004 (Foundational catalog constants)
- **User Story 2 (Phase 4: T009–T011)**: Depends on T004; integrates with US1 in `main.py` (T011)
- **User Story 3 (Phase 5: T012–T013)**: Depends on US1 (T008) and US2 (T010) to harden path and I/O handling
- **Polish (Phase 6: T014–T015)**: Depends on all user stories (T001–T013) being complete

### User Story Dependencies

- **User Story 1 (P1)**: Starts immediately after Phase 2 (T004) — completely independent
- **User Story 2 (P2)**: Core function `carregar_csv` (T009, T010) can start after Phase 2 (T004) in parallel with US1; CLI orchestration in `main.py` (T011) links US1 and US2
- **User Story 3 (P3)**: Extends `gerar_dataset_sintetico` and `carregar_csv` with resilient I/O and nested path handling after T008 and T010

### Within Each User Story (Mandatory TDD Order)

1. Write unit tests in `tests/test_modulo_vendas.py` and confirm they **FAIL** (Red)
2. Implement functions in `gerador_dados.py` / `modulo_vendas.py` / `main.py` to make tests **PASS** (Green)
3. Refactor for clarity, docstrings, and explicit typing while keeping tests green (Refactor)

### Parallel Opportunities

- **Phase 1**: `T002` (`tests/test_modulo_vendas.py` scaffold) and `T003` (`docker-compose.yml`) can run in parallel with `T001` (`requirements.txt`)
- **Phase 3 (US1 Tests)**: `T005`, `T006`, and `T007` can be authored together in `tests/test_modulo_vendas.py` before `T008`
- **Cross-Story**: `T009` (US2 test) and `T012` (US3 test) can be drafted alongside US1 tests

---

## Parallel Example: User Story 1

```bash
# 1. Write all US1 failing tests first (Red Phase):
Task T005: "Write test_gerar_dataset_sintetico_cria_arquivo_e_cabecalho in tests/test_modulo_vendas.py"
Task T006: "Write test_gerar_dataset_sintetico_determinismo_seed in tests/test_modulo_vendas.py"
Task T007: "Write test_gerar_dataset_sintetico_inconsistencias_deliberadas in tests/test_modulo_vendas.py"

# 2. Implement generator to pass all US1 tests (Green Phase):
Task T008: "Implement gerar_dataset_sintetico in gerador_dados.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (`T001`–`T003`)
2. Complete Phase 2: Foundational (`T004`)
3. Complete Phase 3: User Story 1 (`T005`–`T008`)
4. **STOP and VALIDATE**: Run `pytest tests/test_modulo_vendas.py -k "gerar_dataset"` to verify deterministic CSV generation with 100+ records and controlled noise

### Incremental Delivery

1. Setup + Foundational → Base constants ready
2. Add User Story 1 (`gerar_dataset_sintetico`) → Verify via `pytest` (MVP!)
3. Add User Story 2 (`carregar_csv` + `main.py`) → Verify reading & preservation of raw records
4. Add User Story 3 (resilient I/O & nested paths) → Verify edge cases and `vendas.csv` generation
