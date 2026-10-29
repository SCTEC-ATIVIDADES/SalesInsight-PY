# Quickstart: RF03 – Limpar e Tratar os Dados

## Prerequisites

- Python 3.11+
- Project dependencies installed from `requirements.txt`

## Validate the feature

From the repository root, run the focused test module:

```bash
.venv/bin/python -m pytest tests/test_modulo_vendas.py
```

Expected outcome: all tests pass, including scenarios for whitespace normalization, valid numeric conversion, missing/malformed fields, batch invalid-date validation including valid dates outside pandas timestamp bounds, invalid identifiers, missing/blank/invalid numeric values, finite prices, exact-duplicate removal after normalization, primary-reason accounting, input immutability, ordering, and empty input.

Run the complete suite:

```bash
.venv/bin/python -m pytest
```

Expected outcome: the full test suite passes without regressions in existing pipeline stages. The equivalent container check is `docker compose run --rm app python -m pytest`.

## Manual behavior checklist

1. Pass a valid record with surrounding spaces and numeric text; verify cleaned text and converted numeric values.
2. Mix valid rows with rows having missing, blank, or non-convertible quantity/price; verify valid rows remain in order and rejected rows are counted once with a reason.
3. Pass an empty list; verify empty output, zero valid/removed totals, and zero for every reason counter.
4. Compare the input before and after cleaning; it must be unchanged.
5. Include rows with a missing field, null/blank required text, blank or invalid `YYYY-MM-DD` date, invalid identifier, and non-finite price; verify each is rejected once under the documented primary reason.
6. Include an exact duplicate with padded text and a distinct row sharing only the same ID; verify only the exact normalized duplicate is removed and counted as `registro_duplicado`.

See [the data model](data-model.md) and [the function contract](contracts/cleaning-contract.md) for record fields and rejection accounting.
