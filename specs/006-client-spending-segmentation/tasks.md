# Tasks: RF06 – Segmentar Clientes por Nível de Gasto

**Input**: Design documents from `/specs/006-client-spending-segmentation/`

**Prerequisites**: `plan.md`, `spec.md`; supporting decisions and fields in `research.md` and `data-model.md`; no external contracts.

**Tests**: Required by project constitution; follow Red-Green-Refactor in `tests/test_modulo_vendas.py`.

**Organization**: Tasks grouped by the sole user story. Existing repository structure and dependencies mean no setup or foundational changes are needed.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project and Python test infrastructure already exist; no setup task required.

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Existing cleaned sales pipeline provides validated customer and revenue fields; no shared foundation changes required.

## Phase 3: User Story 1 - Identificar segmento de gasto por cliente (Priority: P1) — MVP

**Goal**: Calculate each customer's accumulated purchase total and assign Bronze, Prata, or Ouro.

**Independent Test**: Exercise segmentation with repeated and distinct customers, totals below/at/above both thresholds, and empty input; verify each output total and label independently.

### Tests for User Story 1

- [ ] T001 [US1] Add failing segmentation and pipeline/export acceptance tests in `tests/test_modulo_vendas.py` for repeated purchases, separate customers, exact R$ 3.000 and R$ 8.000 boundaries, totals below/above thresholds, rounded `total_gasto`, empty input, and JSON/CSV inclusion.

### Implementation for User Story 1

- [ ] T002 [US1] Implement reusable customer aggregation and threshold classification in `modulo_vendas.py`; group `receita_total` by `cliente`, accumulate decimal values before classification, return one `{total_gasto, segmento}` result per customer, and round displayed total to two decimals.
- [ ] T003 [US1] Add the segmentation result to the metrics mapping in `main.py` after deriving valid sales, preserving existing JSON `metricas_gerais` wrapper and CSV `Métrica, Valor` export format.

**Checkpoint**: User Story 1 works independently through reusable function and existing CLI exports.

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Verify feature behavior and preserve existing pipeline behavior.

- [ ] T004 Run `pytest tests/test_modulo_vendas.py` and the validation scenarios in `specs/006-client-spending-segmentation/quickstart.md`; fix any failures in the relevant source or test files.

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1) and Foundational (Phase 2) require no changes; repository environment and cleaned sales records already exist.
- User Story 1 follows T001 → T002 → T003. T004 follows all implementation tasks.
- Polish depends on User Story 1 implementation.

### User Story Dependencies

- **User Story 1 (P1)**: No dependency on another story; this is the only story and delivers the MVP.

### Parallel Opportunities

- No safe task-level parallelism: T001 and T002 touch different files but T002 must wait for the tests-first red phase; T003 depends on the function in T002. Independent test cases within T001 may be authored concurrently only if edits are coordinated in the same test file.

## Parallel Example: User Story 1

No tasks are marked `[P]` because each depends on previous TDD or integration work, or shares the same test file.

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Add tests and confirm they fail (T001).
2. Implement minimum reusable segmentation function (T002).
3. Integrate function into CLI metrics/export flow (T003).
4. Run focused tests and quickstart validation (T004).

## Notes

- Every task has checklist, sequential ID, required story label where applicable, and explicit repository file path.
- Segment from accumulated pre-display-rounding totals; Prata includes both boundary values.
- Inputs are assumed cleaned and valid by the existing pipeline.
