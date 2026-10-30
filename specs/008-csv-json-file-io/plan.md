# Implementation Plan: CSV and JSON File I/O

**Branch**: `008-csv-json-file-io` | **Date**: 2026-10-29 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/008-csv-json-file-io/spec.md`

## Summary

RF07 formalizes reusable CSV loading and JSON/CSV export for the existing sales pipeline. Reuse `carregar_csv` and `exportar_resultados` in `modulo_vendas.py`, standard-library `csv`/`json`, UTF-8 file handling, and existing output schemas. Add only focused tests or minimal fixes for uncovered RF07 cases; do not introduce dependencies or break established report contracts.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Python standard library (`csv`, `json`, `os`); existing pandas 2.2.3 and pytest 8.3.4. No new dependencies.

**Storage**: Local UTF-8 CSV input and generated files under `outputs/`.

**Testing**: pytest, primarily `tests/test_modulo_vendas.py`; follow Red-Green-Refactor.

**Target Platform**: Linux, macOS, and Windows with Python 3.11+; existing Docker Compose environment.

**Project Type**: Sales-processing CLI pipeline (`modulo_vendas.py` library functions, `main.py` orchestration).

**Performance Goals**: Load and export the current dataset (approximately 151 records) without unnecessary repeated passes; no measurable delay for normal local use.

**Constraints**: Read CSV as UTF-8 with `csv.DictReader`; export via native `csv` and `json`; preserve current paths `outputs/estatisticas.json`, `outputs/metricas_resumo.csv`, JSON envelope `metricas_gerais`, CSV columns `Métrica, Valor`; create output directory automatically; preserve non-ASCII text; report expected I/O failures clearly. No new output contract or dependency.

**Scale/Scope**: Existing loader/exporter, pipeline integration, focused tests and documentation only; no new storage layer or report format.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Pre-Research | Post-Design | Evidence |
|---|---|---|---|
| I. Modularization | PASS | PASS | Reuse `modulo_vendas.py` functions; `main.py` remains orchestration-only. |
| II. Explicit processing | PASS | PASS | Standard-library CSV/JSON operations and explicit record/metric handling. |
| III. TDD | PASS | PASS | Tests in `tests/test_modulo_vendas.py` precede changes; verify red/green/refactor. |
| IV. Data quality and errors | PASS | PASS | UTF-8 handling and controlled filesystem failure behavior validated; cleaning remains downstream. |
| V. Docker and outputs | PASS | PASS | Existing output names/schemas retained; local and Docker test/run checks documented. |

No gate violations; no complexity exceptions required.

## Project Structure

### Documentation (this feature)

```text
specs/008-csv-json-file-io/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/             # Not needed: internal CLI pipeline, no external interface
```

### Source Code (repository root)

```text
modulo_vendas.py
main.py
tests/
└── test_modulo_vendas.py
README.md
outputs/
├── estatisticas.json
└── metricas_resumo.csv
```

**Structure Decision**: Follow existing single-project CLI layout. File I/O belongs in reusable sales-module functions; tests extend existing module test suite; no contracts directory because no external API or new CLI interface is exposed.

## Complexity Tracking

No constitution violations.
