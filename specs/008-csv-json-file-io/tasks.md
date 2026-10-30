# Tasks: CSV and JSON File I/O

**Input**: Design documents from `/specs/008-csv-json-file-io/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Required by specification and project constitution; use pytest with Red-Green-Refactor.

**Organization**: Tasks grouped by independently testable user story.

## Phase 1: Setup

**Purpose**: Confirm existing project environment; no new scaffolding or dependencies required.

- [ ] T001 Verify Python dependencies and project test command from `requirements.txt` and `tests/test_modulo_vendas.py`

---

## Phase 2: Foundational

**Purpose**: Shared I/O conventions used by both stories.

- [ ] T002 [P] Confirm UTF-8, `newline=""`, and native CSV/JSON usage in `modulo_vendas.py`

---

## Phase 3: User Story 1 - Load sales data (Priority: P1) 🎯 MVP

**Goal**: Read all CSV rows into header-keyed records while preserving text and controlled missing-file behavior.

**Independent Test**: Load temporary CSV fixtures and verify headers, values, accented text, empty input, and missing-file behavior.

### Tests for User Story 1

- [ ] T003 [P] [US1] Add tests for UTF-8 accented values, header-only/empty CSV, and missing/unreadable file behavior in `tests/test_modulo_vendas.py`

### Implementation for User Story 1

- [ ] T004 [US1] Adjust `carregar_csv` in `modulo_vendas.py` only if T003 exposes a mismatch; retain `csv.DictReader`, UTF-8, and existing return contract

**Checkpoint**: Run `pytest -q tests/test_modulo_vendas.py`; CSV loading story works independently.

---

## Phase 4: User Story 2 - Export analysis results (Priority: P1)

**Goal**: Write supplied metrics and customer results as valid UTF-8 JSON and produce existing summary CSV, creating the output directory and replacing prior files.

**Independent Test**: Export known nested metrics and customer data to a temporary folder, reopen both files, and verify content, UTF-8 text, CSV header/rows, and repeated-write replacement.

### Tests for User Story 2

- [ ] T005 [P] [US2] Add export tests for UTF-8 JSON content, CSV headers/rows, empty metrics, auto-created output directory, and file replacement in `tests/test_modulo_vendas.py`

### Implementation for User Story 2

- [ ] T006 [US2] Update `exportar_resultados` in `modulo_vendas.py` only where T005 reveals gaps; preserve filenames, JSON `metricas_gerais` envelope, and CSV `Métrica, Valor` schema
- [ ] T007 [US2] Ensure `main.py` passes full analysis metrics including customer segmentation to exporter without adding business logic

**Checkpoint**: Run `pytest -q tests/test_modulo_vendas.py`; exported files reopen and contain all supplied values.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Validate pipeline, docs, and project quality gates.

- [ ] T008 [P] Document finalized CSV/JSON input and output behavior, filenames, and limitations in `README.md`
- [ ] T009 Run full test suite with `pytest -q` and pipeline with `python main.py`; confirm files under `outputs/`
- [ ] T010 Run `docker compose run --rm app pytest -q` and verify successful completion

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1) → Foundational (Phase 2) → User Stories → Polish.
- US1 and US2 depend only on the shared conventions check; they can proceed independently after Phase 2.

### User Story Dependencies

- **US1 (P1)**: Independent CSV loading flow; no dependency on US2.
- **US2 (P1)**: Independent export flow; no dependency on US1 implementation beyond pipeline's existing metrics input.

### Parallel Opportunities

- T003 and T005 can be implemented in parallel after T001/T002 because they are separate test sections in the same file; avoid concurrent edits if one worker modifies the same test file.
- T008 can proceed in parallel with US implementation in `README.md`.
- US1 implementation and US2 implementation are separately scoped but both touch `modulo_vendas.py`; run sequentially if changing that file to avoid conflicts.

## Parallel Example: User Stories

```text
Task: T003 — add CSV input tests in tests/test_modulo_vendas.py
Task: T005 — add export tests in tests/test_modulo_vendas.py (coordinate to avoid overlapping edits)
Task: T008 — document I/O behavior in README.md
```

## Implementation Strategy

### MVP First

1. Complete setup and shared convention check.
2. Complete US1 tests and minimal implementation; verify CSV loading independently.
3. Add US2 tests and exporter checks; retain established output contracts.
4. Run full local and Docker quality gates.

### Incremental Delivery

US1 and US2 each provide separately verifiable I/O behavior. Deliver US1 first as MVP, then US2, then documentation and full-pipeline validation.
