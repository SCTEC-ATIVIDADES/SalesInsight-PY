# Implementation Plan: RF06 – Segmentar Clientes por Nível de Gasto

**Branch**: `006-client-spending-segmentation` | **Date**: 2026-10-29 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/006-client-spending-segmentation/spec.md`

## Summary

Add reusable customer spending segmentation to `modulo_vendas.py`, grouping cleaned RF04-enriched sales by `cliente` and `receita_total`. Assign Bronze below R$ 3,000, Prata from R$ 3,000 through R$ 8,000 inclusive, and Ouro above R$ 8,000. Wire result through the existing pipeline and generic exports. Follow pytest TDD; add no dependencies.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: pandas 2.2.3 and pytest 8.3.4; segmentation uses standard Python dictionaries and `decimal.Decimal` where exact monetary accumulation is needed. No new dependencies.

**Storage**: N/A; in-memory transformation on cleaned, derived sales records.

**Testing**: pytest in `tests/test_modulo_vendas.py`, mandatory Red-Green-Refactor.

**Target Platform**: Linux / macOS / Windows via Python 3.11+, `.venv`, and existing Docker setup.

**Project Type**: Sales-processing CLI pipeline (`modulo_vendas.py` + `main.py`).

**Performance Goals**: One pass for per-sale accumulation and one pass over customers for classification; support 10,000 sales locally.

**Constraints**: Input has valid, trimmed `cliente` and finite `receita_total`; derived `receita_total` is already rounded per sale to two decimal places. Sum individual sale amounts exactly in decimal form before classification; output `total_gasto` rounded to two decimal places. Threshold boundaries inclusive for Prata. Preserve existing export formats, JSON wrapper `metricas_gerais`, and CSV columns `Métrica, Valor`; add a segmentation key/row without changing existing metrics. No new external interface.

**Scale/Scope**: One reusable segmentation function, pipeline wiring, existing CSV/JSON export inclusion, README documentation, focused tests, and local/Docker validation; no schema or storage changes.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Pre-Research | Post-Design | Evidence |
|---|---|---|---|
| I. Modularization | PASS | PASS | Reusable business logic in `modulo_vendas.py`; `main.py` only orchestrates. |
| II. Explicit processing | PASS | PASS | Explicit loops and dictionaries make grouping and thresholds auditable. |
| III. TDD | PASS | PASS | Tests in `tests/test_modulo_vendas.py` written first; Red-Green-Refactor required. |
| IV. Data quality | PASS | PASS | Function consumes already cleaned/derived records; existing cleaning handles invalid input. |
| V. Docker and outputs | PASS | PASS | Preserve output schemas; verify local and Docker runs; document segmentation and reports in `README.md`. |

No constitution violations; no complexity exceptions.

## Project Structure

### Documentation (this feature)

```text
README.md
specs/006-client-spending-segmentation/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── tasks.md
├── spec.md
└── checklists/requirements.md
```

### Source Code

```text
modulo_vendas.py                # reusable customer segmentation and existing export logic
main.py                         # orchestrates segmentation and export
tests/test_modulo_vendas.py     # segmentation, pipeline, and export tests
outputs/                        # generated CSV and JSON metrics
```

**Structure Decision**: Extend existing single-project CLI pipeline. Reuse existing cleaned/derived records and generic export mechanism; add no modules or dependencies.

## Complexity Tracking

No constitution violations or additional complexity.
