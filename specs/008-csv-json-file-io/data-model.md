# Data Model: CSV and JSON File I/O

## Sales record

- **Fields**: Header names map to raw CSV cell values; values remain strings at ingestion.
- **Relationships**: A collection of records feeds the existing cleaning and sales-analysis stages.
- **Validation**: Header row defines keys. Empty/header-only input yields an empty record collection. Data validation and type conversion remain downstream responsibilities.

## Analysis results

- **Fields**: Overall metrics and customer-level results represented by JSON-compatible mappings, lists, and scalar values.
- **Relationships**: Exported together in the existing statistics document under the established `metricas_gerais` envelope; customer segmentation remains part of the metrics where pipeline supplies it.
- **Validation**: Serialized as valid JSON, preserving non-ASCII text.

## Category summary

- **Fields**: Category label and corresponding revenue total.
- **Relationships**: Derived from existing metric outputs and represented through established CSV export schema (`Métrica, Valor`); no separate output contract is introduced.
- **Validation**: Empty metrics still produce header-only CSV; output is UTF-8 and CSV-escaped.
