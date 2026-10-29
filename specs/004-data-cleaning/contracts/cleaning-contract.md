# Contract: Sales Data Cleaning (RF03)

**Feature**: `004-data-cleaning`
**Module**: `modulo_vendas.py`

## Public function

`limpar_dados(dados_brutos)` accepts an ordered list of raw sales dictionaries and returns a list of cleaned sales dictionaries. It does not mutate the input and prints an aggregate cleaning report.

## Input and output

Input rows use the established eight-field sales schema: `id_venda`, `data_venda`, `cliente`, `produto`, `categoria`, `regiao`, `quantidade`, and `preco_unitario`. Accepted rows retain those fields in the same order and schema. Text fields have surrounding whitespace removed; `id_venda` and `quantidade` are integers; `preco_unitario` is a finite float.

Rows are discarded if quantity or unit price is missing, blank after trimming, or cannot be converted; a row with an invalid identifier is also discarded because the output identifier must be an integer. A rejected row does not stop processing subsequent input rows.

## Reporting and accounting

Prints a report stating valid and removed totals and structured reason counts, attributing each removed row to one primary rejection reason. The function returns only the cleaned list. Valid plus removed equals input count; reason counts sum to removed count.

## Edge behavior

An empty input returns an empty cleaned list and reports zero valid and zero removed. Input dictionaries and their values remain unchanged.
