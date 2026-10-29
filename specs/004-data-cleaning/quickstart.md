# Quickstart: RF03 – Limpar e Tratar os Dados

## Prerequisites

- Python 3.11+
- Project dependencies installed from `requirements.txt`

## Validate the feature

From the repository root, run the focused test module:

```bash
python -m pytest tests/test_modulo_vendas.py
```

Expected outcome: all tests pass, including scenarios for whitespace normalization, valid numeric conversion, missing/blank/invalid numeric fields, rejection accounting, input immutability, ordering, and empty input.

Run the complete suite:

```bash
python -m pytest
```

Expected outcome: the full test suite passes without regressions in existing pipeline stages.

## Manual behavior checklist

1. Pass a valid record with surrounding spaces and numeric text; verify cleaned text and converted numeric values.
2. Mix valid rows with rows having missing, blank, or non-convertible quantity/price; verify valid rows remain in order and rejected rows are counted once with a reason.
3. Pass an empty list; verify empty output and zero counts.
4. Compare the input before and after cleaning; it must be unchanged.

See [the data model](data-model.md) and [the function contract](contracts/cleaning-contract.md) for record fields and rejection accounting.
