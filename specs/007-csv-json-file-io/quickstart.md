# Quickstart: Validate CSV and JSON File I/O

## Prerequisites

- Python 3.11+
- Project dependencies installed from `requirements.txt`

## Local validation

From repository root:

```bash
pytest -q tests/test_modulo_vendas.py
python main.py
```

## Expected outcomes

- Tests pass, including CSV header-to-field mapping, UTF-8 text handling, empty/missing input behavior, exact JSON keys, category CSV rows, and controlled export failures.
- Pipeline completes without an unhandled I/O traceback for expected file errors.
- `outputs/estatisticas.json` is valid UTF-8 JSON with top-level `metricas_gerais` and `clientes` keys.
- `outputs/metricas_resumo.csv` is readable CSV with `Categoria, Receita Total` header and rows from metrics' `por_categoria` mapping.
- Running export into a missing output folder creates it; repeated export replaces prior output files.

## Docker validation

```bash
docker compose run --rm app pytest -q
```

Expected: test suite exits successfully in the project container.
