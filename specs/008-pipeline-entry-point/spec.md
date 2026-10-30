# Feature Specification: RF08 – Executar o Pipeline Completo (Ponto de Entrada)

**Feature Branch**: `008-pipeline-entry-point`

**Created**: 2026-10-29

**Status**: Draft

**Input**: User description: "RF08 – Executar o Pipeline Completo (Ponto de Entrada). No arquivo `main.py`, importar as funções do módulo `modulo_vendas.py` e executar o fluxo de ponta a ponta."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Execute sales analysis end to end (Priority: P1)

As an operator, I can run the application once and receive analyzed sales results and exported files without manually invoking pipeline stages.

**Why this priority**: The entry point makes the existing sales-analysis capabilities usable as a complete workflow.

**Independent Test**: Run the entry point with an existing valid sales dataset; verify pipeline results and output files.

**Acceptance Scenarios**:

1. **Given** a valid sales dataset, **When** the operator runs the entry point, **Then** the application reads, inspects, cleans, transforms, calculates metrics, segments customers, and exports results.
2. **Given** no sales dataset exists, **When** the operator runs the entry point, **Then** a synthetic dataset is generated before processing starts.
3. **Given** export fails, **When** the pipeline finishes, **Then** the failure is reported and success is not reported.

---

### User Story 2 - Keep pipeline orchestration reusable (Priority: P2)

As a developer, I can import the application entry module without starting data processing.

**Why this priority**: Import safety supports testing and reuse without unexpected file changes or console output.

**Independent Test**: Import the entry module in a fresh process and verify no pipeline side effects occur.

**Acceptance Scenarios**:

1. **Given** the entry module is imported, **When** import completes, **Then** the pipeline has not run.
2. **Given** the entry module is executed as the program, **When** processing completes, **Then** the full pipeline runs once.

---

### Edge Cases

- Input dataset is missing and synthetic generation fails.
- Input dataset cannot be read or contains no usable records.
- Output export fails after processing.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Running the application entry point MUST execute the sales workflow end to end using reusable project functions.
- **FR-002**: The workflow MUST generate a synthetic dataset only when the configured input file does not exist.
- **FR-003**: The workflow MUST perform input loading, inspection, cleaning, derived-field transformation, metrics calculation, customer segmentation, and top-customer selection.
- **FR-004**: The workflow MUST display executive summary metrics and the selected top customers.
- **FR-005**: The workflow MUST export analysis results using the established output contract.
- **FR-006**: Importing the entry module MUST NOT execute the pipeline; direct execution MUST invoke it once.
- **FR-007**: Pipeline failures MUST be reported without claiming successful completion.
- **FR-008**: Entry point MUST orchestrate reusable functions and contain no business rules.

### Key Entities

- **Sales dataset**: Input sales records processed by the pipeline.
- **Analysis results**: Aggregate metrics and customer segmentation produced from sales records and exported for inspection.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: One direct application run completes every pipeline stage and produces the established output files when input and output operations succeed.
- **SC-002**: Running with absent input creates the dataset before analysis; existing input is reused without regeneration.
- **SC-003**: Importing the entry module produces no pipeline output or file changes.
- **SC-004**: Failed pipeline operations produce a visible error and no success message.

## Assumptions

- Existing `modulo_vendas.py` functions and RF01–RF07 data/output contracts remain authoritative.
- Default input remains `vendas.csv`; generated data uses 150 records.
- Top-customer selection displays up to five customers with highest spend; ties retain their original customer order.
- If the example’s helper functions are absent, the entry point uses the project’s existing API and does not add duplicate helpers just to match example names.
