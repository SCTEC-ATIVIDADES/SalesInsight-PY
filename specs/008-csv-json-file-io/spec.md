# Feature Specification: CSV and JSON File I/O

**Feature Branch**: `008-csv-json-file-io`

**Created**: 2026-10-29

**Status**: Draft

**Input**: User description: "RF07 – Ler e Escrever Arquivos (CSV e JSON). O código deve ler dados de entrada via `csv.DictReader` e exportar resultados usando os módulos nativos `csv` e `json`."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Load sales data (Priority: P1)

As a user, I can load a sales CSV file and have each row represented as named fields so later processing can use its column names.

**Why this priority**: Reading input starts the sales-analysis workflow.

**Independent Test**: Load a CSV with headers and multiple rows; verify values map to the correct field names.

**Acceptance Scenarios**:

1. **Given** a readable UTF-8 CSV with a header and records, **When** the user loads it, **Then** each record is returned with its header names and corresponding values.
2. **Given** a CSV containing accented text, **When** the user loads it, **Then** text remains intact.

---

### User Story 2 - Export analysis results (Priority: P1)

As a user, I can save overall metrics, customer results, and a category revenue summary as files for inspection or reuse.

**Why this priority**: Persistent outputs deliver the results of the analysis workflow.

**Independent Test**: Export known metrics and customers; reopen both files and verify their contents and category rows.

**Acceptance Scenarios**:

1. **Given** metrics and customer results, **When** the user exports results, **Then** a JSON file contains overall metrics and customers.
2. **Given** category totals, **When** the user exports results, **Then** a CSV file contains a category and revenue header followed by each category total.
3. **Given** the output folder does not exist, **When** the user exports results, **Then** the folder and both files are created.
4. **Given** non-ASCII text in results, **When** the user exports results, **Then** the saved JSON preserves that text in readable form.

### Edge Cases

- A CSV with headers but no data rows returns an empty collection.
- A missing or unreadable input file produces a clear, controlled error and does not emit an unhandled traceback.
- Empty category totals still produce a valid CSV containing its header.
- Existing output files are replaced by the new export; export failure is reported clearly.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST read input sales records from CSV files, using the first row as field names and preserving each row's values under the corresponding names.
- **FR-002**: The system MUST read and write files as UTF-8, preserving accented and other non-ASCII text.
- **FR-003**: The system MUST export overall metrics and customer results together in a JSON document.
- **FR-004**: The system MUST export category revenue totals in a CSV document with columns named `Categoria` and `Receita Total`.
- **FR-005**: The system MUST create the configured output folder when it does not already exist.
- **FR-006**: The system MUST report input/output file failures clearly without exposing an unhandled traceback during normal pipeline execution.
- **FR-007**: The system MUST replace previous output files when writing a new results export.

### Key Entities

- **Sales record**: One input CSV row represented by named fields and their original cell values.
- **Analysis results**: Overall metrics and customer-level results included in the JSON output.
- **Category summary**: Category names paired with their total revenue in the CSV output.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All records in a valid CSV are returned with values assigned to the correct column names, with no rows omitted.
- **SC-002**: Every successful export produces one valid JSON document and one valid category-summary CSV containing all supplied values.
- **SC-003**: Output files preserve non-ASCII text and can be reopened and interpreted without data loss.
- **SC-004**: Export succeeds when the destination folder is absent by creating the folder automatically.

## Assumptions

- CSV input has a header row; values are read as strings for downstream processing.
- Output filenames are `estatisticas.json` and `metricas_resumo.csv`, in an output folder defaulting to `outputs`.
- The project pipeline handles error presentation to the user while reusable file functions expose sufficient failure information to that pipeline.
- Existing sales analysis provides the metrics and customer data to export; this feature does not define how those results are calculated.
