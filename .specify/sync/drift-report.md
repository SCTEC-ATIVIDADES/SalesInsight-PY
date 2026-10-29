# Spec Drift Report

Generated: 2026-10-28T00:00:00Z
Project: SalesInsight-PY

## Summary

| Category | Count |
|----------|-------|
| Specs Analyzed | 2 |
| Requirements Checked | 28 (18 FR + 10 SC) |
| ✓ Aligned | 28 (100%) |
| ⚠️ Drifted | 0 (0%) |
| ✗ Not Implemented | 0 (0%) |
| 🆕 Unspecced Code | 0 |

## Detailed Findings

### Spec: 001-sales-dataset-generator - RF01 – Criar ou Carregar o Dataset de Vendas

#### Aligned ✓
- FR-001: Independent module `gerador_dados.py` implements `gerar_dataset_sintetico(caminho_arquivo="vendas.csv", n_registros=100, seed=42)` using `csv.writer` and UTF-8 (`gerador_dados.py:48-93`).
- FR-002: Header `id_venda,data_venda,cliente,produto,categoria,regiao,quantidade,preco_unitario` written in exact order (`gerador_dados.py:10-19`, `gerador_dados.py:88`).
- FR-003: Generates `>= 100` base records by default (`n_registros=100` in `gerador_dados.py:50`, `n_registros=150` in `main.py:13`) and validates `n_registros >= 1` (`gerador_dados.py:54-55`).
- FR-004: Uses `Faker('pt_BR')` with `fake.seed_instance(seed)` and `random.Random(seed)` (`gerador_dados.py:57-61`) across `PRODUTOS`, `CATEGORIAS`, and `REGIOES`.
- FR-005: Injects controlled inconsistencies: duplicate `dados[0]` (`gerador_dados.py:89`), ~5% empty `quantidade` (`gerador_dados.py:75`), ~5% empty `preco_unitario` (`gerador_dados.py:76-78`), ~10% padded `produto` (`gerador_dados.py:79`).
- FR-006: `carregar_csv(caminho_arquivo="vendas.csv")` implemented in `modulo_vendas.py:16-29` using `csv.DictReader` returning `list[dict[str, str]]`.
- FR-007: Preserves raw strings without premature mutation (`modulo_vendas.py:22-25`, verified in `tests/test_modulo_vendas.py:85-113`).
- FR-008: Resilient `try/except (FileNotFoundError, OSError)` in `modulo_vendas.py:21-28` returning `[]` and printing `[ERRO] Arquivo não encontrado: <caminho_arquivo>`; parent directory creation in `gerador_dados.py:83-84`.
- FR-009: `main.py:9-17` orchestrates conditional dataset generation (`gerar_dataset_sintetico` from `gerador_dados.py`) and loading (`carregar_csv` from `modulo_vendas.py`).
- FR-010: Isolated local `.venv` execution supported and documented in `README.md` and `quickstart.md`, with `.venv/` ignored in `.gitignore:5` and `.dockerignore:5` alongside Docker Compose (`Dockerfile`, `docker-compose.yml`).
- SC-001: Generation and loading of 151 records completes in < 0.1s (`tests/test_modulo_vendas.py`).
- SC-002: 100% deterministic output for identical `seed` (`tests/test_modulo_vendas.py:28-38`).
- SC-003: All 3 categories of noise verified present for `n_registros >= 100` (`tests/test_modulo_vendas.py:41-83`).
- SC-004: 100% of `carregar_csv` records contain all 8 required keys (`tests/test_modulo_vendas.py:109`).
- SC-005: 0 unhandled exceptions on missing files (`tests/test_modulo_vendas.py:115-124`).

#### Drifted ⚠️
None.

#### Not Implemented ✗
None.

### Spec: 002-data-inspection - RF02 – Inspecionar e Descrever os Dados

#### Aligned ✓
- FR-001: `inspecionar_dados(dados)` implemented in `modulo_vendas.py:32-76`.
- FR-002: Prints `\n=== INSPEÇÃO INICIAL DOS DADOS ===` and `Total de registros carregados: {len(dados)}` (`modulo_vendas.py:36-37`).
- FR-003: When `dados` is non-empty, prints `Campos disponíveis: {list(dados[0].keys())}` and `Exemplo do primeiro registro: {dados[0]}` (`modulo_vendas.py:49-52`).
- FR-004: Explicit `for` loop checks `valor is None or (isinstance(valor, str) and valor.strip() == "")` across all fields (`modulo_vendas.py:57-65`).
- FR-005: Prints `Registros com dados incompletos ou nulos: {registros_incompletos}` and `Valores nulos/vazios por campo: {nulos_por_campo}` (`modulo_vendas.py:67-68`).
- FR-006: Returns structured dictionary `ResumoInspecaoDados` with `total_registros`, `campos`, `primeiro_registro`, `registros_incompletos`, and `nulos_por_campo` (`modulo_vendas.py:41-47`, `modulo_vendas.py:70-76`).
- FR-007: Preserves 100% immutability of `dados` during inspection (`tests/test_modulo_vendas.py:240-275`).
- FR-008: Integrated in `main.py:17` (`mv.inspecionar_dados(dados_brutos)` immediately after `mv.carregar_csv`).
- SC-001: Inspection of >= 100 records completes in < 0.05s (`tests/test_modulo_vendas.py`).
- SC-002: 100% accuracy in identifying incomplete rows and per-field null counts (`tests/test_modulo_vendas.py:181-237`).
- SC-003: 0 unhandled exceptions for empty list `[]` (`tests/test_modulo_vendas.py:278-295`).
- SC-004: 100% immutability of input dataset preserved (`tests/test_modulo_vendas.py:240-275`).
- SC-005: 100% of unit tests in `tests/test_modulo_vendas.py` pass (`10 passed`).

#### Drifted ⚠️
None.

#### Not Implemented ✗
None.

### Unspecced Code 🆕
None.

## Inter-Spec Conflicts
None.

## Recommendations
1. Proceed to the next functional requirement (RF03 – Data Cleaning & Transformation) when ready.
