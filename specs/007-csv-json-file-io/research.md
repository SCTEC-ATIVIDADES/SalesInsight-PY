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

- **Decision**: Preserve controlled loader behavior for expected filesystem errors (clear message and empty result); test empty/header-only input, unreadable/missing paths, multi-row mapping, and UTF-8 round-trip. Exporter must propagate write/serialization errors and print success only after both outputs complete; pipeline catches and reports export errors without traceback. Do not suppress serialization failures or claim partial export success.
- **Rationale**: Preserves current loader API and meets RF07 plus constitution's resilient I/O principle. Empty list remains existing loader behavior for failed loads; changing it is outside RF07.
- **Alternatives considered**: Raise all I/O errors to distinguish absence from empty data; rejected for compatibility with existing pipeline and tests.

## Scope resolution

- **Decision**: RF07 supersedes prior generic CSV and nested JSON payload schemas for these output files. Preserve filenames; emit `metricas_gerais` and `clientes` as separate top-level JSON keys; write category CSV required by RF07. Keep sales-record cleaning/validation downstream; this feature tests file parsing/serialization and I/O failures only.
- **Rationale**: Supplied RF07 defines exact keys, columns, and category source. Constitution's data-cleaning/rejection rules belong to existing downstream cleaning feature, not duplicated in this file-I/O change.
- **Alternatives considered**: Keeping generic CSV/nested customer schema fails RF07; duplicating cleaning rules here duplicates ownership.
