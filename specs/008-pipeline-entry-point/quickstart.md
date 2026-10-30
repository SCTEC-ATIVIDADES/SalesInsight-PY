# Quickstart: Validate RF08 Pipeline Entry Point

## Prerequisites

- Python 3.11+ and dependencies from `requirements.txt`, or Docker Engine with Compose v2.
- Run commands from repository root.

## Local validation

```bash
pytest -q
python main.py
```

Expected:

- Tests pass.
- If `vendas.csv` is absent, it is generated before processing; if present, it is reused.
- The pipeline inspects, cleans, transforms, calculates metrics, segments customers, displays summary/top five, and exports outputs.
- `outputs/estatisticas.json` and `outputs/metricas_resumo.csv` remain valid RF07 files.
- Importing `main` alone does not run pipeline or modify files.
- Expected pipeline/export failures are reported; no success message follows a failed run.

## Docker validation

```bash
docker compose run --rm app pytest -q
docker compose run --rm app python main.py
```

Expected: both commands pass and mounted project contains valid RF07 output files after successful pipeline execution.
