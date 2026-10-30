# Implementation Plan: RF05 – Calcular Métricas Agregadas

**Branch**: `005-aggregate-sales-metrics` | **Date**: 2026-10-29 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/005-aggregate-sales-metrics/spec.md`

## Summary

Implement reusable aggregation in `modulo_vendas.py` for revenue by category and region plus company-wide total. Consume RF04-enriched records, compute all metrics in one pass with dictionaries, and include metrics in existing CLI export. Test using pytest/TDD; add no dependencies.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: pandas 2.2.3 and pytest 8.3.4 already installed; aggregation uses Python dictionaries, no new dependencies.

**Storage**: N/A; in-memory transformation on cleaned and derived sales records.

**Testing**: pytest in `tests/test_modulo_vendas.py`, mandatory TDD cycle.

**Target Platform**: Linux / macOS / Windows via Python 3.11+, `.venv`, and existing Docker setup.

**Project Type**: Sales-processing CLI pipeline (`modulo_vendas.py` + `main.py`).

**Performance Goals**: Single O(n) pass; support at least 10,000 records for local execution.

**Constraints**: Input records already contain valid category, region, and finite `receita_total` rounded per sale. Apply Python `round(accumulator + receita_total, 2)` after every grouped addition; sum grand total without intermediate rounding and apply `round(total, 2)` once at return (Python tie-to-even behavior). Group totals need not reconcile exactly with grand total. Add `total_geral`, `por_categoria`, and `por_regiao` inside existing metrics mapping; preserve JSON wrapper `metricas_gerais` and CSV columns `Métrica, Valor`, adding rows/keys only. No external interface; contract files not applicable.

**Scale/Scope**: One reusable aggregation function, pipeline wiring, focused tests, and generated aggregate results; no input schema/storage changes.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Pre-Research | Post-Design | Evidence |
|---|---|---|---|
| I. Modularization | PASS | PASS | Aggregation belongs in reusable `modulo_vendas.py`; `main.py` only orchestrates. |
| II. Explicit processing | PASS | PASS | Native dicts and one explicit loop implement requested aggregation. |
| III. TDD | PASS | PASS | Pytest tests in `tests/test_modulo_vendas.py` written first; red-green-refactor required. |
| IV. Data quality | PASS | PASS | Aggregator consumes records validated by prior cleaning/derivation; no new rejection rules needed. |
| V. Docker and outputs | PASS | PASS | Preserve existing exporter contract and validate local/Docker pipeline outputs. |

No constitution violations; no complexity exceptions.

## Project Structure

### Documentation (this feature)

```text
specs/005-aggregate-sales-metrics/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── spec.md
```

### Source Code

```text
modulo_vendas.py          # reusable aggregation function and existing export logic
tests/test_modulo_vendas.py  # unit and pipeline behavior tests
main.py                   # orchestrates aggregation and export
outputs/                  # generated CSV and JSON metrics
```

**Structure Decision**: Extend existing single-project CLI structure; no new modules or dependencies. The pipeline calls aggregation on RF04-derived records and merges its result into existing exported metrics.

## Complexity Tracking

No constitution violations or additional complexity.
