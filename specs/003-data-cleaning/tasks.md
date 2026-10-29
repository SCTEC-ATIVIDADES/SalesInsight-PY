# Tasks: RF03 – Limpar e Tratar os Dados

**Input**: Design documents from `/specs/003-data-cleaning/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/cleaning-contract.md`

**Tests**: Required by the project constitution; follow Red → Green → Refactor in `tests/test_modulo_vendas.py`.

**Organization**: Tasks are grouped by user story; each story has an independent verification criterion.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm the existing project and test setup; no new infrastructure or dependencies are needed.

- [ ] T001 From the repository root, run `python3 --version` and `python3 -m pytest --version`; confirm Python 3.11+ and pytest are available using `requirements.txt` and `tests/test_modulo_vendas.py` as the project baseline

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No shared infrastructure changes are required; the existing sales schema and module are the foundation.

- [ ] T002 Compare `gerador_dados.py` field constants with the input and output schemas in `specs/003-data-cleaning/data-model.md`; confirm all eight field names match before implementing `limpar_dados` in `modulo_vendas.py`

**Checkpoint**: Existing test harness and record schema are understood; story work can begin.

---

## Phase 3: User Story 1 - Normalizar registros válidos (Priority: P1) - MVP

**Goal**: Produce new, ordered sales records with trimmed text and correctly typed identifier, quantity, and price without mutating raw inputs.

**Independent Test**: Run the US1 tests in `tests/test_modulo_vendas.py`; valid input rows with padded text and numeric strings produce normalized dictionaries with expected field values/types, preserved order, and unchanged raw input.

### Tests for User Story 1

- [ ] T003 [US1] Add failing pytest cases in `tests/test_modulo_vendas.py` for all eight output fields, trimming of `data_venda`, `cliente`, `produto`, `categoria`, and `regiao`, integer identifier and quantity, float unit price, field preservation, ordering, and input immutability

### Implementation for User Story 1

- [ ] T004 [US1] Implement `limpar_dados` in `modulo_vendas.py` with an explicit typed signature and concise docstring; construct fresh output dictionaries, trim `data_venda`, `cliente`, `produto`, `categoria`, and `regiao`, and convert `id_venda`, `quantidade`, and `preco_unitario` as defined in `specs/003-data-cleaning/contracts/cleaning-contract.md`

**Checkpoint**: US1 is independently verified when its focused pytest cases pass and input rows remain unchanged.

---

## Phase 4: User Story 2 - Excluir dados inválidos e reportar o resultado (Priority: P2)

**Goal**: Reject missing, blank, or non-convertible numeric values, continue processing subsequent rows, and report exact aggregate and per-reason counts.

**Independent Test**: Run the US2 tests in `tests/test_modulo_vendas.py`; mixed valid and invalid rows return only accepted records, report valid/removed counts plus primary rejection reason counts, and satisfy `validos + removidos == entradas` and `sum(motivos_remocao) == removidos`.

### Tests for User Story 2

- [ ] T005 [US2] Add failing pytest cases in `tests/test_modulo_vendas.py` for missing/null schema fields, null text, blank `data_venda`, missing/blank/non-convertible quantity and price, non-finite prices, invalid `id_venda`, continued processing, report output, and exactly one primary reason per rejected row (including distinct categories for missing, invalid quantity, invalid price, malformed text/date, and invalid identifier)
- [ ] T006 [US2] Add failing pytest cases in `tests/test_modulo_vendas.py` for empty input, zero totals/reason counts, `validos + removidos == entradas`, and `sum(motivos_remocao) == removidos`

### Implementation for User Story 2

- [ ] T007 [US2] Extend `limpar_dados` in `modulo_vendas.py` to reject absent schema fields, null/blank text, blank or invalid `YYYY-MM-DD` dates, invalid identifiers, missing/blank/invalid numeric fields, and non-finite prices; attribute each rejected row once by the documented schema order and continue processing later rows
- [ ] T008 [US2] Print aggregate valid/removed totals and structured primary-reason counts from `limpar_dados` in `modulo_vendas.py`, including all-zero counters for empty input

**Checkpoint**: US2 is independently verified when all rejection cases are counted once, processing continues, report totals reconcile to input size, and empty input yields no records and all-zero report counters.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Verify the integrated cleaning stage and project regression suite.

- [ ] T009 [P] From the repository root, run `python3 -m pytest tests/test_modulo_vendas.py && python3 -m pytest`; record that both commands exit successfully
- [ ] T010 From the repository root, run `python3 main.py`; verify successful exit and existence of `outputs/metricas_resumo.csv` and `outputs/estatisticas.json`; if missing, record gate V as blocked by out-of-scope pipeline export functionality and do not mark the gate passed
- [ ] T011 From the repository root, run `docker compose up --build --exit-code-from app`; verify successful exit and both expected output files under the mounted `outputs/` directory; if missing, record gate V as blocked by out-of-scope pipeline export functionality and do not mark the gate passed
- [ ] T012 [P] Follow `specs/003-data-cleaning/quickstart.md`; confirm all four manual outcomes (normalized row, invalid-row report, empty list with zero counters, unchanged input) match the documented contract

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; verifies the existing Python/pytest environment.
- **Foundational (Phase 2)**: Depends on setup verification; confirms existing schema and module conventions.
- **User Stories (Phase 3+)**: Begin after the foundation. US1 precedes US2 because US2 extends its cleaning loop and report behavior.
- **Polish (Phase 5)**: Depends on both stories being implemented. T009 (tests) can run independently of T010/T011 (entry point quality gates); T012 (quickstart checks) can run independently of all three.

### User Story Dependencies

- **US1 (P1)**: Starts after Phase 2; no dependency on another story. Delivers the MVP valid-row cleaning behavior.
- **US2 (P2)**: Starts after US1 because rejection validation and reporting extend the same `limpar_dados` function. Tests remain independently verifiable as invalid-row/report behavior.

### Within Each User Story

- Write tests first and verify they fail before implementation, in accordance with TDD.
- Implement only after the corresponding tests are established.
- Run focused tests at each story checkpoint.

### Parallel Opportunities

- No safe parallelism within US1 or US2 because tests and implementation touch the same files and are sequential under TDD.
- After implementation, T009 and T012 can be performed independently; T009 runs the automated regression suites and T012 checks the documented manual scenarios.

---

## Parallel Example: Polish Validation

```text
Task: Run focused/full pytest commands from the repository root (T009)
Task: Validate documented quickstart scenarios against the implementation (T012)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Verify setup and confirm source schema (Phases 1–2).
2. Complete US1 tests first, confirm red, implement normalization/conversion, and confirm green.
3. Stop at the US1 checkpoint: valid rows are normalized and returned without mutation.
4. Continue to US2 for the complete required invalid-row filtering and reporting.

### Incremental Delivery

1. Complete US1 and verify its independent valid-row scenarios.
2. Complete US2 and verify invalid filtering, counts, and reporting.
3. Run integrated quickstart and complete regression checks.

---

## Notes

- Every task follows `- [ ] T### [P?] [US#?] description with file path`.
- `[P]` is used only for independent tasks; none of the story implementation tasks can safely run in parallel because they edit the same module/test file and follow TDD order.
- The function returns the cleaned list; per-reason counts are printed in the report, consistent with the design contract.
