# Tasks: RF08 – Executar o Pipeline Completo (Ponto de Entrada)

**Input**: Design documents from `/specs/008-pipeline-entry-point/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Required by specification and Constitution Principle III. Write tests first, verify red, implement minimum changes, rerun green.

**Organization**: Tasks grouped by independently testable user story.

## Phase 1: Setup

**Purpose**: Confirm existing test and execution commands; no new project setup or dependencies required.

- [ ] T001 Verify pytest and local/Docker entry-point commands in `requirements.txt`, `README.md`, and `docker-compose.yml`

---

## Phase 2: Foundational

**Purpose**: Confirm shared pipeline contracts before story work.

- [ ] T002 [P] Verify RF01–RF07 generator, processing, segmentation, and export interfaces in `gerador_dados.py`, `modulo_vendas.py`, and `specs/007-csv-json-file-io/spec.md`

---

## Phase 3: User Story 1 - Execute sales analysis end to end (Priority: P1) 🎯 MVP

**Goal**: Direct run completes sales processing, shows executive summary and top five customers, and exports RF07 outputs; errors do not claim success.

**Independent Test**: Run `pytest -q tests/test_modulo_vendas.py -k main` with isolated temporary input/output paths and patched pipeline functions; verify stage order, generated-input behavior, summary/top-five display, output invocation, and failure reporting. Then run `python main.py` and validate RF07 output schemas.

### Tests for User Story 1

- [ ] T003 [US1] Add failing `main.py` integration tests for missing-input generation, existing-input reuse, and pipeline stage order in `tests/test_modulo_vendas.py`
- [ ] T004 [US1] Add failing `main.py` output tests for executive summary, highest-spend top-five selection, export call, and no success report on export failure in `tests/test_modulo_vendas.py`

### Implementation for User Story 1

- [ ] T005 [US1] Update `main.py` to orchestrate existing generator and `modulo_vendas.py` stages, display total revenue and up to five highest-spend customers, and invoke RF07 export
- [ ] T006 [US1] Handle expected generation, read, processing, and export failures in `main.py` without traceback or false success message

**Checkpoint**: US1 independently runs full pipeline and preserves established exports.

---

## Phase 4: User Story 2 - Keep pipeline orchestration reusable (Priority: P2)

**Goal**: Importing `main.py` has no pipeline side effects; direct execution runs once.

**Independent Test**: Import `main.py` in a fresh process and verify no output or file changes; execute as `__main__` and assert stage calls occur exactly once.

### Tests for User Story 2

- [ ] T007 [P] [US2] Add failing import-safety and exactly-once direct-execution tests for `main.py` in `tests/test_modulo_vendas.py`

### Implementation for User Story 2

- [ ] T008 [US2] Keep pipeline invocation behind `if __name__ == "__main__":` in `main.py` and satisfy import-safety tests

**Checkpoint**: Both stories independently pass; import never launches work.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Verify full behavior and run documented quality gates.

- [ ] T009 [P] Update RF08 run and expected-output instructions in `README.md`
- [ ] T010 Run `pytest -q`, `python main.py`, and Docker Compose pytest/pipeline commands; verify JSON and CSV schemas per `specs/008-pipeline-entry-point/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1) has no dependencies.
- Foundational (Phase 2) depends on Setup and blocks story tasks.
- US1 (Phase 3) and US2 (Phase 4) follow foundational work; US2 tests are logically independent, but direct-main behavior should be verified after US1 integration.
- Polish (Phase 5) depends on both stories.

### User Story Dependencies

- US1 (P1): MVP; requires foundational contract check only.
- US2 (P2): import safety is independently testable, but shares `main.py` with US1. Avoid parallel implementation edits to that file.

### Parallel Opportunities

- T003 and T004 can be authored in parallel in the same test file only if edits are coordinated; safer sequence is one test-writing task owner.
- T007 can be drafted independently but must be integrated with the same test file after US1 tests.
- T009 documentation can run parallel with `main.py` implementation after contracts are confirmed.

---

## Parallel Example: User Story 1

```text
Task: Add failure-first US1 tests in tests/test_modulo_vendas.py (coordinate one writer for test file)
Task: Review README.md run/output instructions for RF08 documentation update
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Setup and Foundational phases.
2. Write and fail US1 tests; implement the minimum pipeline orchestration and error handling.
3. Validate US1 independently with test doubles, then real local and Docker runs.
4. Add US2 import-safety coverage and confirm import/direct-execution behavior.
5. Complete documentation and final quality gates.

### Incremental Delivery

US1 delivers usable full pipeline and outputs. US2 adds import safety without changing business behavior. Polish verifies docs and both runtime environments.
