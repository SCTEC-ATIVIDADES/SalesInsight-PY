# Spec Drift Report

Generated: 2026-10-28T00:00:00Z
Project: SalesInsight-PY

## Summary

| Category | Count |
|----------|-------|
| Specs Analyzed | 1 |
| Requirements Checked | 14 (9 FR + 5 SC) |
| ✓ Aligned | 14 (100%) |
| ⚠️ Drifted | 0 (0%) |
| ✗ Not Implemented | 0 (0%) |
| 🆕 Unspecced Code | 0 |

## Detailed Findings

### Spec: 001-sales-dataset-generator - RF01 – Criar ou Carregar o Dataset de Vendas

#### Aligned ✓
- FR-001: Independent module `gerador_dados.py` implements `gerar_dataset_sintetico(caminho_arquivo="vendas.csv", n_registros=100, seed=42)` using `csv.writer` and UTF-8 (`gerador_dados.py:48-93`).
- FR-002: Header `id_venda,data_venda,cliente,produto,categoria,regiao,quantidade,preco_unitario` written in exact order (`gerador_dados.py:10-19`, `gerador_dados.py:88`).
- FR-003: Generates `>= 100` base records by default (`n_registros=100` in `gerador_dados.py:50`, `n_registros=150` in `main.py:12`) and validates `n_registros >= 1` (`gerador_dados.py:54-55`).
- FR-004: Uses `Faker('pt_BR')` with `fake.seed_instance(seed)` and `random.Random(seed)` (`gerador_dados.py:57-61`) across `PRODUTOS`, `CATEGORIAS`, and `REGIOES`.
- FR-005: Injects controlled inconsistencies: duplicate `dados[0]` (`gerador_dados.py:89`), ~5% empty `quantidade` (`gerador_dados.py:75`), ~5% empty `preco_unitario` (`gerador_dados.py:76-78`), ~10% padded `produto` (`gerador_dados.py:79`).
- FR-006: `carregar_csv(caminho_arquivo="vendas.csv")` implemented in `modulo_vendas.py:15-27` using `csv.DictReader` returning `list[dict[str, str]]`.
- FR-007: Preserves raw strings without premature mutation (`modulo_vendas.py:21-23`, verified in `tests/test_modulo_vendas.py:82-110`).
- FR-008: Resilient `try/except (FileNotFoundError, OSError)` in `modulo_vendas.py:20-26` returning `[]` and printing `[ERRO] Arquivo não encontrado: <caminho_arquivo>`; parent directory creation in `gerador_dados.py:83-84`.
- FR-009: `main.py:9-15` orchestrates conditional dataset generation (`gerar_dataset_sintetico` from `gerador_dados.py`) and loading (`carregar_csv` from `modulo_vendas.py`).
- SC-001: Generation and loading of 151 records completes in < 0.1s (`tests/test_modulo_vendas.py`).
- SC-002: 100% deterministic output for identical `seed` (`tests/test_modulo_vendas.py:25-33`).
- SC-003: All 3 categories of noise verified present for `n_registros >= 100` (`tests/test_modulo_vendas.py:38-80`).
- SC-004: 100% of `carregar_csv` records contain all 8 required keys (`tests/test_modulo_vendas.py:106`).
- SC-005: 0 unhandled exceptions on missing files (`tests/test_modulo_vendas.py:113-121`).

#### Drifted ⚠️
None.

#### Not Implemented ✗
None.

### Unspecced Code 🆕
None.

## Inter-Spec Conflicts
None (single spec active).

## Recommendations
1. Proceed to the next functional requirement (RF02 – Data Cleaning & Transformation) when ready.
