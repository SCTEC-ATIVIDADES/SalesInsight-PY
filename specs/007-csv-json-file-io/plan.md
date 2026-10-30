# Implementation Plan: CSV and JSON File I/O

**Branch**: `007-csv-json-file-io` | **Date**: 2026-10-29 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/007-csv-json-file-io/spec.md`

## Summary

RF07 formalizes reusable CSV loading and JSON/CSV export for the existing sales pipeline. Reuse `carregar_csv` and `exportar_resultados` in `modulo_vendas.py`, standard-library `csv`/`json`, and UTF-8 file handling. Match RF07 output contracts exactly while keeping existing filenames and avoiding new dependencies.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Python standard library (`csv`, `json`, `os`); existing pandas 2.2.3 and pytest 8.3.4. No new dependencies.

**Storage**: Local UTF-8 CSV input and generated files under `outputs/`.

**Testing**: pytest, primarily `tests/test_modulo_vendas.py`; each behavior change follows Red-Green-Refactor with recorded failing-first and passing-after runs. Final gate runs full pytest suite and `python main.py` locally and through Docker Compose.

**Target Platform**: Linux, macOS, and Windows with Python 3.11+; existing Docker Compose environment.

**Project Type**: Sales-processing CLI pipeline (`modulo_vendas.py` library functions, `main.py` orchestration).

**Performance Goals**: Process current dataset (approximately 151 records) in a single CSV read and category-output pass; no benchmark or latency gate required.

**Constraints**: Read CSV as UTF-8 with `csv.DictReader`; export via native `csv` and `json`; preserve paths `outputs/estatisticas.json` and `outputs/metricas_resumo.csv`; write JSON top-level keys `metricas_gerais` and `clientes`; write category CSV columns `Categoria, Receita Total` with rows from `metricas["por_categoria"]`; create output directory automatically; preserve non-ASCII text; report expected I/O failures clearly. No new dependencies.

**Scale/Scope**: Existing loader/exporter, pipeline integration, focused tests and documentation only; RF07 defines JSON payload and category CSV schemas.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Pre-Research | Post-Design | Evidence / Scope |
|---|---|---|---|
| I. Modularization | PASS | PASS | I/O remains in reusable functions in `modulo_vendas.py`; `main.py` only orchestrates under main guard. New/changed functions retain concise docstrings and explicit typed signatures. |
| II. Explicit processing | PASS | PASS | CSV/JSON use Python standard library; no opaque processing or new dependencies. |
| III. TDD | PASS | PASS | T003/T005/T006 write tests first; each test task requires a failing run before implementation, then green run before refactor. Error paths included. |
| IV. Data quality and errors | PASS (scoped) | PASS (scoped) | This feature tests file-format and filesystem failures, reporting without false success. Sales validation, cleaning, rejection counts, and malformed record handling remain owned by existing downstream cleaning feature and are not claimed as covered here. |
| V. Docker and outputs | PASS | PASS | Local and Docker gates each run tests plus `python main.py`; verify JSON/CSV artifacts. README documents objective, prerequisites/setup, Docker, TDD, CSV rationale, output structure, concepts, and limitations. |

No feature-scope gate violations; no complexity exceptions required.

## Project Structure

### Documentation (this feature)

```text
specs/007-csv-json-file-io/
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

No constitution violations. Feature scope excludes sales-data validation/rejection logic, which remains owned by downstream cleaning; plan claims only file-format, filesystem-error, and export-contract coverage.
