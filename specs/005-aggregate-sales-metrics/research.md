# Research: RF05 – Calcular Métricas Agregadas

## Decision: Aggregation and rounding

Group totals by category and region are rounded to two decimals after each addition; grand total is accumulated from the per-sale rounded `receita_total` values and rounded once at the end.

**Rationale**: Matches provided RF05 assignment example. RF04 rounds each sale before aggregation. Group and grand totals intentionally use distinct rounding sequences; no reconciliation guarantee or error bound is part of the contract. Python `round` uses ties-to-even.

**Alternatives considered**: Round all totals only at the end, or use decimal arithmetic. Neither matches the supplied example or project’s existing Python `round` behavior.

## Decision: Data structures and complexity

Use native dictionaries and one explicit pass over the input list; no new dependency.

**Rationale**: Explicitly requested by RF05 and consistent with Constitution II. A single pass computes category, region, and general totals in O(n).

**Alternatives considered**: Pandas groupby or multiple passes; unnecessary for this requirement and less aligned with the requested educational implementation.

## Decision: Pipeline integration

Call aggregation after derived revenue fields are produced, then include returned metric values in the existing metrics dictionary passed to the exporter.

**Rationale**: The current CLI is the user-facing pipeline and the constitution requires structured, traceable metric outputs. The generic exporter already accepts nested metric dictionaries.

**Alternatives considered**: Keep the function isolated and omit results from outputs; would make requested metrics unavailable during normal pipeline execution.

## Decision: Validation

Use the existing pytest suite in `tests/test_modulo_vendas.py`; include empty, repeated groups, multiple groups, rounding, and one-pass/large-list coverage. Validate local and Docker execution under the project’s existing quality gates.

**Rationale**: Required by Constitution III and existing project conventions.

**Alternatives considered**: New test module or framework; unnecessary.
