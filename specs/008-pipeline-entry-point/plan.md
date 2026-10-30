# Implementation Plan: RF08 – Executar o Pipeline Completo (Ponto de Entrada)

**Branch**: `008-pipeline-entry-point` | **Date**: 2026-10-29 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/008-pipeline-entry-point/spec.md`

## Summary

RF08 delivers a usable end-to-end sales workflow through the existing Python entry point. Keep `main.py` as a thin orchestration layer: use the existing data generator and reusable sales functions, print the executive summary/top customers, preserve RF07 exports, and report failures without claiming success. No new dependency or abstraction needed.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Standard library, existing pandas 2.2.3, Faker 40.43.0; pytest 8.3.4. No new dependencies.

**Storage**: Local `vendas.csv`; generated `outputs/estatisticas.json` and `outputs/metricas_resumo.csv`.

**Testing**: pytest in `tests/test_modulo_vendas.py`; preserve TDD. Final gates: `pytest -q`, `python main.py`, Docker Compose pytest and `python main.py`.

**Target Platform**: Linux, macOS, Windows; Docker Compose.

**Project Type**: Python CLI pipeline.

**Performance Goals**: Process the existing ~151-row dataset end-to-end; no added latency benchmark.

**Constraints**: Keep business logic in reusable modules; `main.py` only orchestrates behind `if __name__ == "__main__"`; generate input only when absent; preserve RF07 output filenames/schemas; report errors without false success; no dependencies.

**Scale/Scope**: Existing dataset and pipeline; touch `main.py` and `tests/test_modulo_vendas.py` only if implementation gaps require it.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- I. Modularization/separation: PASS — orchestration in `main.py`, reusable behavior in `modulo_vendas.py`, generation in `gerador_dados.py`.
- II. Explicit processing: PASS — existing stages use clear Python control flow and pandas where applicable; no opaque pipeline framework proposed.
- III. Mandatory TDD: PASS — implementation changes require tests-first Red-Green-Refactor in `tests/test_modulo_vendas.py`.
- IV. Resilient data/errors: PASS — reuse cleaning and error handling; test pipeline failure reporting and no false success.
- V. Docker/output traceability: PASS — preserve established outputs and validate locally and in Docker Compose.

No gate violations; no waivers required.

## Project Structure

### Documentation (this feature)

```text
specs/008-pipeline-entry-point/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── tasks.md
```

### Source Code (repository root)

```text
main.py
modulo_vendas.py
gerador_dados.py
tests/test_modulo_vendas.py
```

**Structure Decision**: Existing single-project layout. RF08 is entry-point orchestration; avoid new modules and dependencies.

## Phase 0: Research

Resolved project choices and current implementation in [research.md](./research.md). All unknowns resolved.

## Phase 1: Design & Contracts

- Data entities and invariants: [data-model.md](./data-model.md).
- No external interface contract: this is an internal CLI workflow without a stable argument/API surface.
- Runnable validation path: [quickstart.md](./quickstart.md).

## Constitution Check (Post-Design)

- I. Modularization/separation: PASS — design keeps entry point orchestration thin and reuses dedicated modules.
- II. Explicit processing: PASS — no new processing abstraction or dependency.
- III. Mandatory TDD: PASS — tests-first changes and full pytest gate specified.
- IV. Resilient data/errors: PASS — failures are covered and success is emitted only after successful completion.
- V. Docker/output traceability: PASS — RF07 output contracts and Docker validation preserved.

No design violations; no complexity waivers required.
