# Research: CSV and JSON File I/O

## CSV input

- **Decision**: Use Python's standard `csv.DictReader` over a UTF-8 text file opened with `newline=""`; preserve cell values as strings and return one mapping per record.
- **Rationale**: Matches RF07, current `carregar_csv`, and existing test expectations; no additional dependency.
- **Alternatives considered**: pandas CSV parsing is unnecessary for this boundary and would not satisfy explicit DictReader requirement. `csv.reader` lacks direct header-to-field mapping.

## Exports

- **Decision**: Keep JSON serialization via `json.dump` with UTF-8 and `ensure_ascii=False`; write CSV using `csv.writer`, UTF-8, and `newline=""`; create output folder before writing. Keep existing output filenames and JSON wrapper unless spec-level consumers require a change.
- **Rationale**: Native modules are explicit RF07 requirement; current project already establishes filenames and generic output schemas, with tests depending on them.
- **Alternatives considered**: `csv.DictWriter` is unnecessary for the existing two-column output; third-party serializers add no value.

## Errors and empty input

- **Decision**: Preserve controlled loader behavior for expected filesystem errors (clear message and empty result); ensure tests cover empty/header-only input, unreadable/missing paths, and UTF-8 text. Let JSON serialization errors remain visible to the pipeline's normal error handling rather than silently emitting partial success.
- **Rationale**: Consistent with current API and constitution's resilient I/O principle. Empty list is existing behavior for failed load, although it conflates missing input with valid empty input; changing that contract is outside RF07 without a specified caller migration.
- **Alternatives considered**: Raise all I/O errors to distinguish absence from empty data; rejected for compatibility with existing pipeline and tests.

## Scope resolution

- **Decision**: Follow the feature specification's named outputs and schemas only where compatible with established project contracts; RF07's example category/revenue CSV conflicts with existing `Métrica, Valor` CSV schema, existing plan/specs require preserving output formats. Preserve existing schemas and include supplied metrics/customer segmentation through the established generic metrics structure; do not add new output files.
- **Rationale**: Project constitution and prior aggregate/segmentation specs require stable output paths/schema; no downstream contract change specified.
- **Alternatives considered**: Replace existing CSV with category-only rows and JSON payload contract with explicit customer key; rejected as breaking existing consumers. Clarify during implementation if RF07 is intended to supersede prior output contracts.
