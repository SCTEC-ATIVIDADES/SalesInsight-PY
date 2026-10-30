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

- [X] T001 [US1] Add failing segmentation and pipeline/export acceptance tests in `tests/test_modulo_vendas.py` for repeated purchases, separate customers, exact R$ 3.000 and R$ 8.000 boundaries, totals below/above thresholds, rounded `total_gasto`, empty input, and JSON/CSV inclusion.

### Implementation for User Story 1

- [X] T002 [US1] Implement reusable customer aggregation and threshold classification in `modulo_vendas.py`; group `receita_total` by `cliente`, accumulate decimal values before classification, return one `{total_gasto, segmento}` result per customer, and round displayed total to two decimals.
- [X] T003 [US1] Add the segmentation result to the metrics mapping in `main.py` after deriving valid sales, preserving existing JSON `metricas_gerais` wrapper and CSV `Métrica, Valor` export format.

**Checkpoint**: User Story 1 works independently through reusable function and existing CLI exports.

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Verify feature behavior and preserve existing pipeline behavior.

- [X] T004 [P] Update `README.md` to document customer spending segmentation thresholds and inclusion in existing CSV/JSON reports.
- [X] T005 [P] Run `.venv/bin/python -m pytest tests/test_modulo_vendas.py` and `.venv/bin/python main.py`; verify `outputs/metricas_resumo.csv` and `outputs/estatisticas.json` contain segmentation while preserving existing schemas, fixing failures in the relevant files.
- [X] T006 [P] Run `docker compose run --rm app pytest -v` and `docker compose up --build`; verify tests pass and generated output files include segmentation without errors.

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1) and Foundational (Phase 2) require no changes; repository environment and cleaned sales records already exist.
- User Story 1 follows T001 → T002 → T003.
- T004, T005, and T006 depend on User Story 1 implementation. T005/T006 validate independently; T004 is documentation-only.

### User Story Dependencies

- **User Story 1 (P1)**: No dependency on another story; this is the only story and delivers the MVP.

### Parallel Opportunities

- T001, T002, and T003 are sequential due to TDD and integration dependencies.
- After T003, T004, T005, and T006 can run independently: README documentation, local validation, and Docker validation touch separate resources.

## Parallel Example: User Story 1

After T003 completes, run T004 (README documentation), T005 (local validation), and T006 (Docker validation) concurrently; tasks touch or verify separate resources.

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Add tests and confirm they fail (T001).
2. Implement minimum reusable segmentation function (T002).
3. Integrate function into CLI metrics/export flow (T003).
4. Document segmentation and existing reports in README (T004).
5. Run focused tests and local pipeline validation (T005).
6. Run Docker tests and pipeline validation (T006).

## Notes

- Every task has checklist, sequential ID, required story label where applicable, and explicit repository file path.
- Segment from accumulated pre-display-rounding totals; Prata includes both boundary values.
- Inputs are assumed cleaned and valid by the existing pipeline.
- T005/T006 validate constitution-required local and Docker quality gates.

## Phase 5: Convergence

- [X] T007 Add tests for Bronze below R$ 3,000, single-purchase classification, and negative valid totals per US1/AC1 and Edge Cases (partial).
- [X] T008 Add 10,000-sale performance test for `segmentar_clientes_por_gasto` per plan: Performance Goals (partial).
- [X] T009 Complete README documentation of TDD flow, CSV-reading rationale, output structure, applied concepts, and known limitations per Constitution V (partial).
