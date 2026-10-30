# Quickstart: Validate CSV and JSON File I/O

## Prerequisites

- Python 3.11+
- Project dependencies installed from `requirements.txt`

## Local validation (TDD quality gate)

Write focused tests first, run them and confirm expected failure. Implement minimum change, rerun tests to green, then refactor. For final gate, from repository root:

```bash
pytest -q
python main.py
```

## Expected outcomes

- Tests pass, including multi-row CSV source order and exact header-to-value mapping, UTF-8 read/write round-trip, empty/missing input behavior, exact JSON keys, category CSV rows, and controlled export failures.
- Pipeline reports expected input/output I/O failures clearly without an unhandled traceback or false export-success message.
- `outputs/estatisticas.json` is valid UTF-8 JSON with top-level `metricas_gerais` and `clientes` keys.
- `outputs/metricas_resumo.csv` is readable CSV with `Categoria, Receita Total` header and rows from metrics' `por_categoria` mapping.
- Running export into a missing output folder creates it; repeated export replaces prior output files.

## Docker validation

```bash
docker compose run --rm app pytest -q
docker compose run --rm app python main.py
```

Expected: both commands exit successfully; mounted project contains valid `outputs/estatisticas.json` and `outputs/metricas_resumo.csv` with RF07 schemas.

Repeat the same two commands locally (`pytest -q`, `python main.py`) before merge.
