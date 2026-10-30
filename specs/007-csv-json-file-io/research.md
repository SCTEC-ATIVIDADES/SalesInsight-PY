# Research: CSV and JSON File I/O

## CSV input

- **Decision**: Use Python's standard `csv.DictReader` over a UTF-8 text file opened with `newline=""`; preserve cell values as strings and return one mapping per record.
- **Rationale**: Matches RF07, current `carregar_csv`, and existing test expectations; no additional dependency.
- **Alternatives considered**: pandas CSV parsing is unnecessary for this boundary and would not satisfy explicit DictReader requirement. `csv.reader` lacks direct header-to-field mapping.

## Exports

- **Decision**: Serialize `{"metricas_gerais": metricas, "clientes": clientes}` via `json.dump` with UTF-8 and `ensure_ascii=False`; write CSV using `csv.writer`, UTF-8, and `newline=""`, with `Categoria, Receita Total` header and rows from `metricas["por_categoria"].items()`. Keep existing output filenames and create output folder before writing.
- **Rationale**: Native modules and these payload/column contracts are explicit RF07 requirements; existing output filenames remain compatible.
- **Alternatives considered**: `csv.DictWriter` is unnecessary for the existing two-column output; third-party serializers add no value.

## Errors and empty input

- **Decision**: Preserve controlled loader behavior for expected filesystem errors (clear message and empty result); ensure tests cover empty/header-only input, unreadable/missing paths, and UTF-8 text. Let JSON serialization errors remain visible to the pipeline's normal error handling rather than silently emitting partial success.
- **Rationale**: Consistent with current API and constitution's resilient I/O principle. Empty list is existing behavior for failed load, although it conflates missing input with valid empty input; changing that contract is outside RF07 without a specified caller migration.
- **Alternatives considered**: Raise all I/O errors to distinguish absence from empty data; rejected for compatibility with existing pipeline and tests.

## Scope resolution

- **Decision**: RF07 supersedes the prior generic CSV and nested JSON payload schemas for these two existing output files. Preserve filenames, emit customer results as the explicit `clientes` JSON key, and write the category-specific CSV required by RF07.
- **Rationale**: The supplied RF07 definition explicitly specifies JSON keys, CSV columns, and category source; implementation artifacts must match that contract.
- **Alternatives considered**: Keeping the generic metrics CSV and nested customer segmentation would not satisfy RF07.
