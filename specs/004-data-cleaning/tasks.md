# Tasks: RF03 – Limpar e Tratar os Dados

**Input**: Design documents from `/specs/004-data-cleaning/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/cleaning-contract.md`

**Tests**: Required by the project constitution; follow Red → Green → Refactor in `tests/test_modulo_vendas.py`.

**Organization**: Tasks are grouped by user story; each story has an independent verification criterion.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm the existing project and test setup; no new infrastructure or dependencies are needed.

- [ ] T001 Verify existing Python and pytest setup against `requirements.txt` and `tests/test_modulo_vendas.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No shared infrastructure changes are required; the existing sales schema and module are the foundation.

- [ ] T002 Review the eight-field sales schema in `gerador_dados.py` and existing public-function conventions in `modulo_vendas.py` before adding the cleaning function

**Checkpoint**: Existing test harness and record schema are understood; story work can begin.

---

## Phase 3: User Story 1 - Normalizar registros válidos (Priority: P1) - MVP

**Goal**: Produce new, ordered sales records with trimmed text and correctly typed identifier, quantity, and price without mutating raw inputs.

**Independent Test**: Run the US1 tests in `tests/test_modulo_vendas.py`; valid input rows with padded text and numeric strings produce normalized dictionaries with expected field values/types, preserved order, and unchanged raw input.

### Tests for User Story 1

- [ ] T003 [US1] Add failing pytest cases for valid-row text trimming, integer identifier and quantity, float unit price, field preservation, ordering, and input immutability in `tests/test_modulo_vendas.py`

### Implementation for User Story 1

- [ ] T004 [US1] Implement `limpar_dados` in `modulo_vendas.py` to construct fresh output dictionaries from valid rows, trim `data_venda`, `cliente`, `produto`, `categoria`, and `regiao`, and convert `id_venda`, `quantidade`, and `preco_unitario` to the types defined in `specs/004-data-cleaning/contracts/cleaning-contract.md`

**Checkpoint**: US1 is independently verified when its focused pytest cases pass and input rows remain unchanged.

---

## Phase 4: User Story 2 - Excluir dados inválidos e reportar o resultado (Priority: P2)

**Goal**: Reject missing, blank, or non-convertible numeric values, continue processing subsequent rows, and report exact aggregate and per-reason counts.

**Independent Test**: Run the US2 tests in `tests/test_modulo_vendas.py`; mixed valid and invalid rows return only accepted records, report valid/removed counts plus primary rejection reason counts, and satisfy `validos + removidos == entradas` and `sum(motivos_remocao) == removidos`.

### Tests for User Story 2

- [ ] T005 [US2] Add failing pytest cases in `tests/test_modulo_vendas.py` for missing, null, empty, whitespace-only, and non-convertible `quantidade` and `preco_unitario`, non-finite prices, invalid `id_venda`, continued processing, aggregate report output, and additive primary-reason counts

### Implementation for User Story 2

- [ ] T006 [US2] Extend `limpar_dados` in `modulo_vendas.py` to reject rows with absent, blank, or invalid numeric fields (and invalid `id_venda`), attribute each rejected row to one primary reason, and continue the loop after rejection
- [ ] T007 [US2] Print valid, removed, and structured primary-reason counts from `limpar_dados` in `modulo_vendas.py`, including zero counts for empty input

**Checkpoint**: US2 is independently verified when all rejection cases are counted once, processing continues, and report totals reconcile to the input size.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Verify the integrated cleaning stage and project regression suite.

- [ ] T008 [P] Run focused and complete pytest suites from the repository root using `python -m pytest tests/test_modulo_vendas.py` and `python -m pytest`
- [ ] T009 [P] Validate the documented cleaning scenarios in `specs/004-data-cleaning/quickstart.md` against the implementation and update the guide only if behavior differs

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; verifies the existing Python/pytest environment.
- **Foundational (Phase 2)**: Depends on setup verification; confirms existing schema and module conventions.
- **User Stories (Phase 3+)**: Begin after the foundation. US1 precedes US2 because US2 extends its cleaning loop and report behavior.
- **Polish (Phase 5)**: Depends on both stories being implemented.

### User Story Dependencies

- **US1 (P1)**: Starts after Phase 2; no dependency on another story. Delivers the MVP valid-row cleaning behavior.
- **US2 (P2)**: Starts after US1 because rejection validation and reporting extend the same `limpar_dados` function. Tests remain independently verifiable as invalid-row/report behavior.

### Within Each User Story

- Write tests first and verify they fail before implementation, in accordance with TDD.
- Implement only after the corresponding tests are established.
- Run focused tests at each story checkpoint.

### Parallel Opportunities

- No safe parallelism within US1 or US2 because tests and implementation touch the same files and are sequential under TDD.
- After implementation, T008 and T009 can be performed independently; T008 is marked `[P]` because it changes no files and T009 may only edit the quickstart guide.

---

## Parallel Example: Polish Validation

```text
Task: Run focused/full pytest commands from the repository root (T008)
Task: Validate documented quickstart scenarios against the implementation (T009)
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
