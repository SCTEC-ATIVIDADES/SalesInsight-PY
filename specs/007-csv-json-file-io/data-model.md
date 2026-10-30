# Data Model: CSV and JSON File I/O

## Sales record

- **Fields**: Header names map to raw CSV cell values; values remain strings at ingestion.
- **Relationships**: A collection of records feeds the existing cleaning and sales-analysis stages.
- **Validation**: Header row defines keys. Empty/header-only input yields an empty record collection. Data validation and type conversion remain downstream responsibilities.

## Analysis results

- **Fields**: `metricas_gerais` (overall metrics) and `clientes` (customer results), each represented by JSON-compatible mappings, lists, or scalar values.
- **Relationships**: Exported together in the statistics document as separate top-level `metricas_gerais` and `clientes` keys. The exporter receives metrics and customer results separately.
- **Validation**: Serialized as valid JSON, preserving non-ASCII text.

## Category summary

- **Fields**: Category label and corresponding revenue total; CSV header exactly `Categoria, Receita Total`.
- **Relationships**: Derived from `metricas["por_categoria"]` and written as one CSV row per category.
- **Validation**: Empty category totals still produce header-only CSV; output is UTF-8 and CSV-escaped.
