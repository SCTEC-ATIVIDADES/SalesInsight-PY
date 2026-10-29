---

description: "Task list for RF02 – Inspecionar e Descrever os Dados implementation"
---

# Tasks: RF02 – Inspecionar e Descrever os Dados

**Input**: Design documents from `/specs/002-data-inspection/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Included as REQUIRED by Constitution Principle III (Desenvolvimento Orientado a Testes - TDD INEGOCIÁVEL). All test tasks MUST be written first and fail before implementation.

**Organization**: Tasks are grouped by user story (`US1`, `US2`, `US3`) to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Root modules**: `modulo_vendas.py` (implementação de `inspecionar_dados`), `main.py` (orquestração do pipeline), `gerador_dados.py` (gerador RF01), `vendas.csv` at repository root
- **Tests**: `tests/test_modulo_vendas.py`
- **Documentation**: `README.md` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify baseline test suite and typing imports in `modulo_vendas.py` per `plan.md`.

- [X] T001 Verify existing RF01 test suite passes in `tests/test_modulo_vendas.py` and import `Any` from `typing` in `modulo_vendas.py` to support explicit return type annotations (`dict[str, Any]`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Define the function signature, docstring, and return structure contract for `inspecionar_dados` in `modulo_vendas.py` that all user stories build upon.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [X] T002 Define `inspecionar_dados(dados: list[dict[str, str | None]]) -> dict[str, Any]` signature and docstring in `modulo_vendas.py` matching `contracts/inspection-contract.md` and `data-model.md` entity `ResumoInspecaoDados` (`total_registros: int`, `campos: list[str]`, `primeiro_registro: dict[str, str | None] | None`, `registros_incompletos: int`, `nulos_por_campo: dict[str, int]`)

**Checkpoint**: Foundation ready - user story implementation can now begin in priority order.

---

## Phase 3: User Story 1 - Exibição do Panorama Geral e Estrutura Inicial dos Dados Carregados (Priority: P1) 🎯 MVP

**Goal**: Exibir no console o cabeçalho `=== INSPEÇÃO INICIAL DOS DADOS ===`, o total de registros carregados (`Total de registros carregados: {len(dados)}`), a lista de campos disponíveis (`Campos disponíveis: {list(dados[0].keys())}`) e o exemplo do primeiro registro (`Exemplo do primeiro registro: {dados[0]}`), retornando essas informações estruturadas no dicionário de resumo e integrando a chamada em `main.py`.

**Independent Test**: Executar `.venv/bin/pytest tests/test_modulo_vendas.py -k "inspecionar_dados_exibe_panorama"` e verificar via `capsys` e retorno da função que o cabeçalho, total de registros, lista das 8 colunas na ordem original e primeiro registro são exibidos e retornados com exatidão.

### Tests for User Story 1 (TDD - Red Phase) ⚠️

> **NOTE: Write this test FIRST in `tests/test_modulo_vendas.py`, ensure it FAILS before implementing `inspecionar_dados` logic**

- [X] T003 [P] [US1] Write unit test `test_inspecionar_dados_exibe_panorama_e_estrutura_inicial` in `tests/test_modulo_vendas.py` verifying console output (`\n=== INSPEÇÃO INICIAL DOS DADOS ===`, `Total de registros carregados: 2`, `Campos disponíveis: ['id_venda', 'data_venda', 'cliente', 'produto', 'categoria', 'regiao', 'quantidade', 'preco_unitario']`, `Exemplo do primeiro registro:`) and returned `ResumoInspecaoDados` keys (`total_registros == 2`, `campos == gd.CABECALHO_VENDAS`, `primeiro_registro == dados[0]`)

### Implementation for User Story 1 (TDD - Green & Refactor Phase)

- [X] T004 [US1] Implement initial structural inspection in `inspecionar_dados` in `modulo_vendas.py` printing `\n=== INSPEÇÃO INICIAL DOS DADOS ===`, `Total de registros carregados: {len(dados)}`, and when `if dados:` printing `Campos disponíveis: {list(dados[0].keys())}` and `Exemplo do primeiro registro: {dados[0]}` while populating `total_registros`, `campos`, and `primeiro_registro` in the returned dictionary
- [X] T005 [US1] Integrate `mv.inspecionar_dados(dados_brutos)` call in `main.py` immediately after `dados_brutos = mv.carregar_csv(arquivo_dados)` per `contracts/inspection-contract.md` and `FR-008`

**Checkpoint**: At this point, User Story 1 is functional, integrated in `main.py`, and testable independently.

---

## Phase 4: User Story 2 - Verificação e Contabilização de Linhas com Dados Incompletos ou Nulos (Priority: P2)

**Goal**: Verificar todos os registros carregados para identificar e contabilizar linhas com dados incompletos ou nulos (`None`, `""` ou apenas espaços em branco `valor.strip() == ""`), exibindo o total de registros incompletos e a contagem de nulos por campo no console e retornando ambos no dicionário de resumo sem modificar os dados de entrada.

**Independent Test**: Executar `.venv/bin/pytest tests/test_modulo_vendas.py -k "incompletos or imutabilidade"` e verificar que linhas com `""`, `"   "` ou `None` (incluindo múltiplos campos vazios na mesma linha) são contabilizadas exatamente uma vez em `registros_incompletos`, detalhadas em `nulos_por_campo`, e que a lista original permanece 100% inalterada.

### Tests for User Story 2 (TDD - Red Phase) ⚠️

- [X] T006 [P] [US2] Write unit test `test_inspecionar_dados_contabiliza_linhas_incompletas_e_nulos_por_campo` in `tests/test_modulo_vendas.py` verifying rule `"Um valor v é considerado incompleto/nulo se e somente se v is None ou (isinstance(v, str) and v.strip() == '')"` across records with empty string `""`, whitespace-only `"   "`, `None`, and multiple missing fields on the same row (`0 <= registros_incompletos <= total_registros`, `0 <= nulos_por_campo[c] <= total_registros`), plus console output lines `Registros com dados incompletos ou nulos:` and `Valores nulos/vazios por campo:`
- [X] T007 [P] [US2] Write unit test `test_inspecionar_dados_preserva_imutabilidade_da_entrada` in `tests/test_modulo_vendas.py` verifying rule `"A coleção dados e cada dicionário interno não podem sofrer qualquer alteração durante inspecionar_dados(dados)"` and that a dataset with all valid fields reports `registros_incompletos == 0`

### Implementation for User Story 2 (TDD - Green & Refactor Phase)

- [X] T008 [US2] Implement explicit `for` loop null/incomplete verification in `inspecionar_dados` in `modulo_vendas.py` checking `valor is None or (isinstance(valor, str) and valor.strip() == "")` for each field in `campos`, incrementing `nulos_por_campo[campo]` and counting each row with at least one missing field once in `registros_incompletos`, printing `Registros com dados incompletos ou nulos: {registros_incompletos}` and `Valores nulos/vazios por campo: {nulos_por_campo}` without mutating `dados`

**Checkpoint**: At this point, User Stories 1 AND 2 work independently and pass all inspection and completeness assertions.

---

## Phase 5: User Story 3 - Comportamento Seguro para Coleção de Dados Vazia (Priority: P3)

**Goal**: Garantir que `inspecionar_dados([])` execute com segurança sem tentar acessar `dados[0]`, exibindo `Total de registros carregados: 0` e `Registros com dados incompletos ou nulos: 0` e retornando o resumo zerado (`total_registros=0`, `campos=[]`, `primeiro_registro=None`, `registros_incompletos=0`, `nulos_por_campo={}`).

**Independent Test**: Executar `.venv/bin/pytest tests/test_modulo_vendas.py -k "lista_vazia"` e verificar que `inspecionar_dados([])` não levanta `IndexError`, omite `Campos disponíveis` e `Exemplo do primeiro registro`, e retorna o dicionário zerado.

### Tests for User Story 3 (TDD - Red Phase) ⚠️

- [X] T009 [P] [US3] Write unit test `test_inspecionar_dados_lista_vazia_executa_sem_erro` in `tests/test_modulo_vendas.py` verifying constraint `"Se len(dados) == 0, nenhuma tentativa de acesso a dados[0] é realizada"`, stdout contains `Total de registros carregados: 0` and `Registros com dados incompletos ou nulos: 0` (without `Campos disponíveis:` or `Exemplo do primeiro registro:`), and return value equals `{"total_registros": 0, "campos": [], "primeiro_registro": None, "registros_incompletos": 0, "nulos_por_campo": {}}`

### Implementation for User Story 3 (TDD - Green & Refactor Phase)

- [X] T010 [US3] Ensure empty-collection branch in `inspecionar_dados` in `modulo_vendas.py` safely handles `dados == []` by printing `Registros com dados incompletos ou nulos: 0` and returning `{"total_registros": 0, "campos": [], "primeiro_registro": None, "registros_incompletos": 0, "nulos_por_campo": {}}`

**Checkpoint**: All user stories (`US1`, `US2`, `US3`) are independently functional and tested.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: End-to-end validation with `main.py` and documentation update per `quickstart.md`.

- [X] T011 Run full pytest suite (`.venv/bin/pytest tests/test_modulo_vendas.py -v`) and CLI pipeline (`.venv/bin/python main.py`) to validate all `specs/002-data-inspection/quickstart.md` scenarios
- [X] T012 [P] Update `README.md` at repository root to document `inspecionar_dados(dados)` (RF02) usage, console output format, and returned diagnostic summary structure

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1: T001)**: No dependencies - can start immediately
- **Foundational (Phase 2: T002)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3: T003–T005)**: Depends on Foundational (`T002`)
- **User Story 2 (Phase 4: T006–T008)**: Depends on `T004` (extends `inspecionar_dados` in `modulo_vendas.py`)
- **User Story 3 (Phase 5: T009–T010)**: Depends on `T008` (verifies and finalizes empty-list guard in `inspecionar_dados`)
- **Polish (Phase 6: T011–T012)**: Depends on all user stories (`T001`–`T010`) being complete

### User Story Dependencies

- **User Story 1 (P1)**: Starts immediately after Phase 2 (`T002`) — delivers MVP structural inspection and `main.py` integration
- **User Story 2 (P2)**: Builds on `inspecionar_dados` from US1 to add completeness/null scanning per row and per column
- **User Story 3 (P3)**: Validates and hardens the empty-dataset boundary condition (`dados == []`) on `inspecionar_dados`

### Within Each User Story (Mandatory TDD Order)

1. Write unit tests in `tests/test_modulo_vendas.py` and confirm they **FAIL** (Red)
2. Implement logic in `modulo_vendas.py` / `main.py` to make tests **PASS** (Green)
3. Refactor for clarity, docstrings, and explicit typing while keeping tests green (Refactor)

### Parallel Opportunities

- **Test Authoring**: Unit tests `T003` (US1), `T006` & `T007` (US2), and `T009` (US3) can be drafted in parallel before or during TDD Red phases
- **Polish**: `T012` (`README.md` update) can run in parallel with `T011` (quickstart validation)

---

## Parallel Example: User Story 2

```bash
# 1. Write US2 failing tests in parallel (Red Phase):
Task T006: "Write test_inspecionar_dados_contabiliza_linhas_incompletas_e_nulos_por_campo in tests/test_modulo_vendas.py"
Task T007: "Write test_inspecionar_dados_preserva_imutabilidade_da_entrada in tests/test_modulo_vendas.py"

# 2. Implement completeness & null verification (Green Phase):
Task T008: "Implement explicit for loop null/incomplete verification in inspecionar_dados in modulo_vendas.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (`T001`)
2. Complete Phase 2: Foundational (`T002`)
3. Complete Phase 3: User Story 1 (`T003`–`T005`)
4. **STOP and VALIDATE**: Run `.venv/bin/pytest tests/test_modulo_vendas.py -k "inspecionar_dados_exibe_panorama"` to confirm the core RF02 example output works end-to-end

### Incremental Delivery

1. Setup + Foundational → Function signature and contract ready
2. Add User Story 1 (Structural panorama + `main.py`) → Test independently (MVP!)
3. Add User Story 2 (Incomplete/null row & column counting + immutability check) → Test independently
4. Add User Story 3 (Safe empty list handling `[]`) → Test independently
5. Polish (`README.md` + full `quickstart.md` validation)
