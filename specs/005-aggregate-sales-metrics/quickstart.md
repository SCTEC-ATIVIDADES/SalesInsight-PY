# Quickstart: Validate Aggregated Metrics

## Prerequisites

- Python 3.11+ and project dependencies installed from `requirements.txt`.
- Run commands from repository root.

## Validation

1. Run focused tests: `pytest tests/test_modulo_vendas.py`.
2. Confirm category and region aggregation, general total, two-decimal rounding, and empty-input behavior.
3. Run full suite: `pytest`.
4. Run pipeline: `python main.py`; confirm successful completion and metric files under `outputs/`.
5. Validate Docker: `docker compose run --rm --entrypoint pytest app` and `docker compose run --rm app`.

## References

- Requirements: [spec.md](./spec.md)
- Input/output entities: [data-model.md](./data-model.md)
- Rounding and design decisions: [research.md](./research.md)
