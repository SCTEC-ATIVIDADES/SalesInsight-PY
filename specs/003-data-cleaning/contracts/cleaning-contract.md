# Contract: Sales Data Cleaning (RF03)

**Feature**: `003-data-cleaning`
**Module**: `modulo_vendas.py`

## Public function

`limpar_dados(dados_brutos)` accepts an ordered list of raw sales dictionaries and returns a list of cleaned sales dictionaries. It does not mutate the input and prints an aggregate cleaning report.

## Input and output

Input rows use the established eight-field sales schema: `id_venda`, `data_venda`, `cliente`, `produto`, `categoria`, `regiao`, `quantidade`, and `preco_unitario`. Accepted rows retain those fields in the same order and schema. Text fields have surrounding whitespace removed; `id_venda` and `quantidade` are integers; `preco_unitario` is a finite float.

Rows are discarded if any expected schema field is absent; a text field is null; `data_venda` is blank after trimming; `id_venda` cannot be converted to integer; quantity or unit price is missing, blank, or not convertible; or unit price is non-finite. Non-empty dates must be valid calendar dates in `YYYY-MM-DD` format. A rejected row does not stop processing subsequent input rows.

## Reporting and accounting

Prints valid and removed totals plus structured counts for primary rejection reasons: `campo_ausente`, `campo_textual_invalido`, `data_venda_invalida`, `id_venda_invalido`, `quantidade_ausente`, `preco_unitario_ausente`, `quantidade_invalida`, and `preco_unitario_invalido`. When multiple issues apply, attribute the row once to the earliest reason in validation order: missing fields; text fields (`data_venda`, `cliente`, `produto`, `categoria`, `regiao`); invalid date; quantity; price; identifier (converted after other fields, matching the established record construction order). The function returns only the cleaned list. Valid plus removed equals input count; reason counts sum to removed count.

## Edge behavior

An empty input returns an empty cleaned list and reports zero valid and zero removed. Input dictionaries and their values remain unchanged.
