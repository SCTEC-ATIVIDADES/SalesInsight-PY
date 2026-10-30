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

**Independent Test**: Call `calcular_metricas` on minimal records containing only `categoria` and `receita_total`; verify category totals rounded to two decimals, without region aggregation.

### Tests

- [X] T001 [US1] Add category tests using minimal records with only `categoria` and `receita_total`, covering repeated/distinct categories and per-addition rounding in `tests/test_modulo_vendas.py`; run first and confirm failure.

### Implementation

- [X] T002 [US1] Implement `calcular_metricas(dados)` category aggregation in `modulo_vendas.py`, using `categoria` as key and rounding accumulated totals to two decimals after each addition.

**Checkpoint**: Category totals independently pass focused tests.

## Phase 4: User Story 2 - Consultar receita por região (Priority: P2)

**Goal**: Calculate rounded revenue total per region.

**Independent Test**: Call `calcular_metricas` on minimal records containing only `regiao` and `receita_total`; verify each regional sum and two-decimal rounding, without category aggregation.

### Tests

- [X] T003 [US2] Add region tests using minimal records with only `regiao` and `receita_total`, covering repeated/distinct regions and per-addition rounding in `tests/test_modulo_vendas.py`; run first and confirm failure.

### Implementation

- [X] T004 [US2] Extend `calcular_metricas(dados)` in `modulo_vendas.py` to aggregate `receita_total` by `regiao` in same input pass, rounding each group accumulator after addition.

**Checkpoint**: Category and region totals both pass focused tests.

## Phase 5: User Story 3 - Consultar receita total da empresa (Priority: P3)

**Goal**: Calculate company-wide revenue and expose all aggregate metrics in pipeline outputs.

**Independent Test**: Call `calcular_metricas` on minimal records containing only `receita_total`; verify `total_geral` without category/region fields. Separately test pipeline export integration after full result shape exists.

### Tests

- [X] T005 [US3] Add grand-total rounding test using records with only `receita_total`, plus empty-input (`0.0`, empty groups) and full result-shape tests in `tests/test_modulo_vendas.py`; run first and confirm failure.
- [X] T006 [US3] Add pipeline integration test verifying aggregated metrics are passed to `exportar_resultados` in `tests/test_modulo_vendas.py`.

### Implementation

- [X] T007 [US3] Complete `calcular_metricas(dados)` in `modulo_vendas.py` with a grand total accumulated across all records and rounded to two decimals at return.
- [X] T008 [US3] Call `mv.calcular_metricas(dados_com_campos_derivados)` and merge its result into existing `metricas` before export in `main.py`, preserving existing exporter format.

**Checkpoint**: Full metric dictionary and pipeline export pass independently.

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validate all stories together and confirm one-pass scale target.

- [X] T009 [P] Add a deterministic 10,000-record test in `tests/test_modulo_vendas.py`: record `i` has `categoria=f'C{i % 10}'`, `regiao=f'R{i % 4}'`, `receita_total=1.00`; assert `total_geral == 10000.0`, each of 10 categories totals `1000.0`, each of 4 regions totals `2500.0`.
- [X] T010 Run focused suite, full pytest suite, `python main.py`, and Docker validations specified in `specs/005-aggregate-sales-metrics/quickstart.md`.

## Phase 7: Precision Hardening

**Purpose**: Prevent binary floating-point drift in aggregation while preserving specified per-addition rounding.

- [X] T011 [US1] Add adversarial large-count and fractional-cent rounding tests in `tests/test_modulo_vendas.py` to lock exact accumulation behavior.
- [X] T012 [US1] Use exact decimal accumulation in `calcular_metricas` in `modulo_vendas.py`, retaining Python `round` semantics and float output shape.

## Phase 8: Convergence

- [X] T013 Reconcile duplicate T011/T012 entries and duplicate Phase 7 headings; original Phase 7 Precision Hardening contains authoritative completed T011/T012 entries. No duplicate IDs remain.

## Dependencies & Execution Order

### Phase Dependencies

- Setup and Foundational have no work; existing project infrastructure is ready.
- User stories are ordered by priority. Shared function signature is introduced in US1, then extended in US2 and US3.
- Polish depends on all three stories.

### User Story Dependencies

- **US1 (P1)**: Independent MVP; starts immediately.
- **US2 (P2)**: Test-only behavior is independently specified with records containing only `regiao` and `receita_total`; implementation may extend `calcular_metricas` introduced by US1.
- **US3 (P3)**: Grand-total behavior is independently specified with records containing only `receita_total`; full return-shape and CLI export integration depend on US1/US2 outputs.

### Parallel Opportunities

- T001 and T003 test authoring can be drafted independently, but implementation is sequential because stories extend same function and module.
- T005 and T006 test work may be parallelized if coordinated to avoid concurrent edits to `tests/test_modulo_vendas.py`; otherwise execute sequentially.
- T009 may run after implementation and does not alter source code.
- T011 test authoring precedes T012 implementation; both modify the existing test/module files sequentially.

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
- Aggregation input comes from RF04 output; Python `round` (ties-to-even) applies after each grouped addition; grand total rounds once at end. Group totals need not reconcile exactly with grand total.
- No external contract files apply to this internal CLI feature.
