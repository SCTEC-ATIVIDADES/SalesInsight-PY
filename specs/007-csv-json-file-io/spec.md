# Feature Specification: CSV and JSON File I/O

**Feature Branch**: `007-csv-json-file-io`

**Created**: 2026-10-29

**Status**: Draft

**Input**: User description: "RF07 – Ler e Escrever Arquivos (CSV e JSON). O código deve ler dados de entrada via `csv.DictReader` e exportar resultados usando os módulos nativos `csv` e `json`."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Load sales data (Priority: P1)

As a user, I can load a sales CSV file and have each row represented as named fields so later processing can use its column names.

**Why this priority**: Reading input starts the sales-analysis workflow.

**Independent Test**: Load a CSV with headers and multiple rows; verify values map to the correct field names.

**Acceptance Scenarios**:

1. **Given** a readable UTF-8 CSV with a header and at least two records, **When** the user loads it, **Then** every record is returned as a mapping with each header paired to its original cell value, in source order, with no omitted rows.
2. **Given** a CSV containing accented text, **When** the user loads it, **Then** text remains intact.

---

### User Story 2 - Export analysis results (Priority: P1)

As a user, I can save overall metrics, customer results, and a category revenue summary as files for inspection or reuse.

**Why this priority**: Persistent outputs deliver the results of the analysis workflow.

**Independent Test**: Export known metrics and customers; reopen both files and verify their contents and category rows.

**Acceptance Scenarios**:

1. **Given** metrics and customer results, **When** the user exports results, **Then** a JSON file contains top-level `metricas_gerais` and `clientes` keys with supplied values.
2. **Given** metrics containing category totals, **When** the user exports results, **Then** a CSV file has header `Categoria, Receita Total` followed by each entry from `metricas["por_categoria"]`.
3. **Given** the output folder does not exist, **When** the user exports results, **Then** the folder and both files are created.
4. **Given** non-ASCII text in results, **When** the user exports results, **Then** the saved JSON preserves that text in readable form.

### Edge Cases

- A CSV with headers but no data rows returns an empty collection.
- A missing or unreadable input file produces a clear error, returns the existing empty-list result, and does not emit an unhandled traceback.
- An output-path or serialization failure is surfaced to the pipeline; no success message is printed for files not successfully written. Pipeline reports the failure clearly without an unhandled traceback.
- Empty category totals still produce a valid CSV containing its header.
- Existing output files are replaced by the new export; export failure is reported clearly.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST read input sales records with Python's native `csv.DictReader`, using the first row as field names and preserving every row's original values under corresponding names.
- **FR-002**: The system MUST read CSV and write JSON/CSV as UTF-8 using Python's native `csv` and `json` modules, preserving accented and other non-ASCII text in supported fields and values.
- **FR-003**: The system MUST export a JSON document with top-level keys `metricas_gerais` for overall metrics and `clientes` for customer results.
- **FR-004**: The system MUST export each category and revenue total from `metricas["por_categoria"].items()` as a row in a CSV document with header `Categoria, Receita Total`.
- **FR-005**: The system MUST create the configured output folder when it does not already exist.
- **FR-006**: The loader MUST retain existing behavior for expected input filesystem failures: print a clear error and return an empty list. The exporter MUST surface write/serialization failures; the pipeline MUST report failures clearly without printing success for incomplete exports or exposing an unhandled traceback during normal execution.
- **FR-007**: The system MUST replace previous output files when writing a new results export.

### Key Entities

- **Sales record**: One input CSV row represented by named fields and their original cell values.
- **Analysis results**: Overall metrics and customer-level results included in the JSON output.
- **Category summary**: Category names paired with their total revenue in the CSV output.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All records in a valid CSV are returned with values assigned to the correct column names, with no rows omitted.
- **SC-002**: Every successful export produces one valid JSON document and one valid category-summary CSV containing all supplied values.
- **SC-003**: Input and output fixtures containing non-ASCII text reopen with identical field names and values, without data loss.
- **SC-004**: Export succeeds when the destination folder is absent by creating the folder automatically.

## Assumptions

- CSV input has a header row; values are read as strings for downstream processing.
- Output filenames are `estatisticas.json` and `metricas_resumo.csv`, in an output folder defaulting to `outputs`.
- The project pipeline handles error presentation to the user while reusable file functions expose sufficient failure information to that pipeline.
- Existing sales analysis provides the metrics and customer data to export; this feature does not define how those results are calculated.
