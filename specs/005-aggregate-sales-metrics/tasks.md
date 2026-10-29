# Tasks: RF05 – Calcular Métricas Agregadas

**Input**: Design documents from `/specs/005-aggregate-sales-metrics/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `quickstart.md`

**Tests**: Required by specification and Constitution III; follow Red → Green → Refactor in `tests/test_modulo_vendas.py`.

## Phase 1: Setup

**Purpose**: No project initialization or dependency changes needed; existing Python, pytest, and Docker setup is reused.

## Phase 2: Foundational

**Purpose**: No blocking prerequisites; RF04 provides enriched records and existing exporter accepts metric dictionaries.

## Phase 3: User Story 1 - Consultar receita por categoria (Priority: P1) — MVP

**Goal**: Calculate rounded revenue total per category from RF04-enriched sales.

**Independent Test**: Call `calcular_metricas` on records with repeated and distinct categories; verify category totals rounded to two decimals.

### Tests

- [ ] T001 [US1] Add category aggregation tests for repeated categories, distinct categories, and two-decimal accumulation in `tests/test_modulo_vendas.py`; run them first and confirm failure.

### Implementation

- [ ] T002 [US1] Implement `calcular_metricas(dados)` category aggregation in `modulo_vendas.py`, using `categoria` as key and rounding accumulated totals to two decimals after each addition.

**Checkpoint**: Category totals independently pass focused tests.

## Phase 4: User Story 2 - Consultar receita por região (Priority: P2)

**Goal**: Calculate rounded revenue total per region.

**Independent Test**: Call `calcular_metricas` on records with repeated and distinct regions; verify each regional sum and two-decimal rounding.

### Tests

- [ ] T003 [US2] Add regional aggregation tests for repeated and distinct regions in `tests/test_modulo_vendas.py`; run them first and confirm failure.

### Implementation

- [ ] T004 [US2] Extend `calcular_metricas(dados)` in `modulo_vendas.py` to aggregate `receita_total` by `regiao` in same input pass, rounding each group accumulator after addition.

**Checkpoint**: Category and region totals both pass focused tests.

## Phase 5: User Story 3 - Consultar receita total da empresa (Priority: P3)

**Goal**: Calculate company-wide revenue and expose all aggregate metrics in pipeline outputs.

**Independent Test**: Verify aggregate dictionary has `total_geral`, `por_categoria`, and `por_regiao`; run pipeline and confirm exported metrics include these values.

### Tests

- [ ] T005 [US3] Add tests for grand-total rounding, empty input (`0.0` and empty groups), and complete returned result shape in `tests/test_modulo_vendas.py`; run first and confirm failure.
- [ ] T006 [US3] Add pipeline integration test verifying aggregated metrics are passed to `exportar_resultados` in `tests/test_modulo_vendas.py`.

### Implementation

- [ ] T007 [US3] Complete `calcular_metricas(dados)` in `modulo_vendas.py` with a grand total accumulated across all records and rounded to two decimals at return.
- [ ] T008 [US3] Call `mv.calcular_metricas(dados_com_campos_derivados)` and merge its result into existing `metricas` before export in `main.py`, preserving existing exporter format.

**Checkpoint**: Full metric dictionary and pipeline export pass independently.

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validate all stories together and confirm one-pass scale target.

- [ ] T009 [P] Add a 10,000-record aggregation test asserting expected totals and group counts in `tests/test_modulo_vendas.py`.
- [ ] T010 Run focused suite, full pytest suite, `python main.py`, and Docker validations specified in `specs/005-aggregate-sales-metrics/quickstart.md`.

## Dependencies & Execution Order

### Phase Dependencies

- Setup and Foundational have no work; existing project infrastructure is ready.
- User stories are ordered by priority. Shared function signature is introduced in US1, then extended in US2 and US3.
- Polish depends on all three stories.

### User Story Dependencies

- **US1 (P1)**: Independent MVP; starts immediately.
- **US2 (P2)**: Depends on `calcular_metricas` introduced by US1; extends same function.
- **US3 (P3)**: Depends on aggregated return structure from US1/US2; integrates results into CLI export.

### Parallel Opportunities

- T001 and T003 test authoring can be drafted independently, but implementation is sequential because stories extend same function and module.
- T005 and T006 test work may be parallelized if coordinated to avoid concurrent edits to `tests/test_modulo_vendas.py`; otherwise execute sequentially.
- T009 may run after implementation and does not alter source code.

## Parallel Example: User Story 1

```text
Task: Add category aggregation tests in tests/test_modulo_vendas.py
Task: Review expected category rounding cases against specs/005-aggregate-sales-metrics/data-model.md
```

## Implementation Strategy

### MVP First

1. No setup/foundation work required.
2. Complete US1 and validate category totals independently.
3. Stop at MVP checkpoint if category metrics alone are sufficient for demonstration.

### Incremental Delivery

1. US1 adds category revenue totals.
2. US2 adds regional revenue totals.
3. US3 adds company total and makes all metrics available in exported pipeline outputs.
4. Run all quickstart checks after the integrated result is complete.

## Notes

- Every task uses checkbox, sequential ID, applicable story label, and explicit file path.
- TDD tasks must fail before corresponding implementation.
- Aggregation input comes from RF04 output; category/region group totals round after each addition, grand total rounds once at end.
- No external contract files apply to this internal CLI feature.
