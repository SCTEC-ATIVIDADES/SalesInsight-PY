# Research: RF03 – Limpar e Tratar os Dados

## Decision 1: Numeric acceptance and rejection

- **Decision**: Treat `quantidade` as valid only when it can be converted to an integer and `preco_unitario` only when it can be converted to a finite floating-point value. Strip surrounding whitespace before checking/converting. Reject a row when either value is missing, blank, or invalid; continue processing later rows.
- **Rationale**: Matches the requested conversions and invalid-row filtering while avoiding non-finite prices (`NaN`, infinities) in subsequent analysis. The current CSV dataset uses decimal-point prices.
- **Alternatives considered**: Accept non-finite float strings (rejected because they are not usable unit prices); normalize locale-specific decimal separators (out of scope and ambiguous without an input convention).

## Decision 2: Row transformation and source preservation

- **Decision**: Construct a fresh cleaned dictionary for each accepted record, preserving input order and trimming the text fields in the existing eight-column sales schema. Convert `id_venda` to integer as shown in the provided example; if its conversion fails, reject the malformed row rather than aborting the collection.
- **Rationale**: Follows the example and established dataset schema, ensures a stable downstream record shape, and protects raw input from mutation.
- **Alternatives considered**: Mutating source dictionaries (rejected by the feature’s data-preservation expectation); retaining the identifier as text (rejected because the example explicitly converts it).

## Decision 3: Rejection accounting and user report

- **Decision**: Return only cleaned rows, as specified. Print aggregate valid/removed counts and structured primary-reason counts in the cleaning report. Categories are `campo_ausente`, `campo_textual_invalido`, `data_venda_invalida`, `id_venda_invalido`, `quantidade_ausente`, `preco_unitario_ausente`, `quantidade_invalida`, and `preco_unitario_invalido`. A row failing multiple checks is removed once; select the first reason deterministically using schema order.
- **Rationale**: Preserves the requested list return contract and satisfies the constitution’s requirement for reason-level structured rejection accounting without adding dependencies.
- **Alternatives considered**: Adding the reason map to the function return (rejected because the requested/example return is the cleaned list); only a scalar removed count (rejected because it loses the mandated reason detail).

## Technical context confirmation

- Python 3.11+, `pytest` already pinned in `requirements.txt`; no additional dependency or storage required.
- Existing input schema and test location are confirmed by `gerador_dados.py`, `modulo_vendas.py`, and `tests/test_modulo_vendas.py`.
- No unresolved technical clarification remains.
