# Tasks: CSV and JSON File I/O

**Input**: Design documents from `/specs/007-csv-json-file-io/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Required by specification and project constitution. For each behavior change, write tests first, run them and confirm expected failures, implement minimum change, then rerun to green before refactoring (Red-Green-Refactor). Record test command and red/green result in task completion notes.

**Organization**: Tasks grouped by independently testable user story.

## Phase 1: Setup

**Purpose**: Confirm existing project environment; no new scaffolding or dependencies required.

- [X] T001 Verify Python dependencies and project test command from `requirements.txt` and `tests/test_modulo_vendas.py`

---

## Phase 2: Foundational

**Purpose**: Shared I/O conventions used by both stories.

- [X] T002 [P] Confirm UTF-8, `newline=""`, and native CSV/JSON usage in `modulo_vendas.py`

---

## Phase 3: User Story 1 - Load sales data (Priority: P1) 🎯 MVP

**Goal**: Read all CSV rows into header-keyed records while preserving text and controlled missing-file behavior.

**Independent Test**: Load a UTF-8 temporary CSV with at least two rows; verify every row returned in source order, exact header-to-cell mappings, accented values, empty/header-only input, and missing/unreadable-file behavior.

### Tests for User Story 1

- [X] T003 [P] [US1] Add tests using a UTF-8 CSV with at least two records to assert all rows, source order, exact header-to-value mapping, and accented values; also test header-only/empty input plus missing/unreadable path in `tests/test_modulo_vendas.py`. Docker run `pytest -q tests/test_modulo_vendas.py -k carregar_csv`: 4 passed, including simulated `PermissionError`; loader behavior already satisfied tests, so no artificial code change.

### Implementation for User Story 1

- [X] T004 [US1] Confirm existing `carregar_csv` in `modulo_vendas.py` already meets T003 using `csv.DictReader`, UTF-8, and current empty-list error contract; no source change needed (T003 run: 3 passed).

**Checkpoint**: Run `pytest -q tests/test_modulo_vendas.py`; CSV loading story works independently.

---

## Phase 4: User Story 2 - Export analysis results (Priority: P1)

**Goal**: Write supplied metrics and customer results as valid UTF-8 JSON with top-level `metricas_gerais` and `clientes` keys; produce category CSV using `Categoria, Receita Total` and `metricas["por_categoria"]`, creating the output directory and replacing prior files.

**Independent Test**: Export known metrics containing `por_categoria` and separate customer results to a temporary folder, reopen both files, and verify exact JSON keys/values, UTF-8 text, CSV header/rows, repeated-write replacement, and clearly reported export failures.

### Tests for User Story 2

- [X] T005 [US2] Add export tests for exact JSON keys/values (`metricas_gerais`, `clientes`), UTF-8 round-trip, exact category CSV header and every `por_categoria` row, empty categories, auto-created output directory, and file replacement in `tests/test_modulo_vendas.py`; Docker focused run was red against old exporter, then passed after T007.
- [X] T006 [US2] Add exporter write/serialization failure tests and no-success assertion in `tests/test_modulo_vendas.py`; serialization failure and unusable output path propagate without `[OK]` output.

### Implementation for User Story 2

- [X] T007 [US2] Implement minimum `exportar_resultados` changes in `modulo_vendas.py` to accept metrics/customers separately, write JSON keys `metricas_gerais` and `clientes`, export all `metricas["por_categoria"]` rows under `Categoria, Receita Total`, preserve filenames, and surface write/serialization failures without false success; focused exporter tests passed after the red run.
- [X] T008 [US2] Add pipeline export-failure test first in `tests/test_modulo_vendas.py`, confirm red (`OSError` traceback), update `main.py` to pass metrics/customer results separately and report failure clearly without business logic; rerun test green (1 passed).

**Checkpoint**: Run `pytest -q tests/test_modulo_vendas.py`; exported files reopen and contain all supplied values.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Validate pipeline, docs, and project quality gates.

- [X] T009 [P] Document project objective, prerequisites/install, local and Docker setup, TDD workflow, CSV/JSON rationale, output files/schema, concepts, and known limitations in `README.md`; update obsolete architecture/output descriptions.
- [ ] T010 Run `pytest -q` and `python main.py`; verify `outputs/estatisticas.json` keys and `outputs/metricas_resumo.csv` header/category rows locally. Blocked: host Python lacks pandas (`ModuleNotFoundError`); Docker validation passed.
- [X] T011 Run `docker compose run --rm app pytest -q` and `docker compose run --rm app python main.py`; verify JSON keys and CSV header/category rows in mounted `outputs/` (`53 passed`; both output schemas inspected).

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1) → Foundational (Phase 2) → User Stories → Polish.
- US1 and US2 depend only on shared conventions and can proceed independently after Phase 2; run implementation tasks only after their tests have recorded red results.

### User Story Dependencies

- **US1 (P1)**: Independent CSV loading flow; no dependency on US2.
- **US2 (P1)**: Independent export flow; consumes metrics and customer results assembled by the existing pipeline.

### Parallel Opportunities

- T003 and T005 can be implemented in parallel after T001/T002 because they are separate test sections in the same file; avoid concurrent edits if one worker modifies the same test file.
- T009 can proceed in parallel with US implementation; documentation review after T010.
- US1 implementation and US2 implementation are separately scoped but both touch `modulo_vendas.py`; run sequentially if changing that file to avoid conflicts.

## Parallel Example: User Stories

```text
Task: T003 — write CSV input tests first in tests/test_modulo_vendas.py; confirm red
Task: T005/T006 — write export success/failure tests first in tests/test_modulo_vendas.py; confirm red
Task: T009 — document I/O behavior in README.md
```

## Implementation Strategy

### MVP First

1. Complete setup and shared convention check.
2. Complete US1 tests and minimal implementation; verify CSV loading independently.
3. Add US2 tests and exporter checks; implement RF07 JSON and category CSV contracts.
4. Run full local and Docker quality gates.

### Incremental Delivery

US1 and US2 each provide separately verifiable I/O behavior. Deliver US1 first as MVP, then US2, then documentation and full-pipeline validation. For every changed behavior: tests first → confirm red → minimum implementation → confirm green → refactor.
