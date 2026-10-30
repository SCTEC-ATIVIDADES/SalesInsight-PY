# Contract: Sales Data Cleaning (RF03)

**Feature**: `003-data-cleaning`
**Module**: `modulo_vendas.py`

## Public function

`limpar_dados(dados_brutos, resumo_remocao=None)` accepts an ordered list of raw sales dictionaries and returns a list of cleaned sales dictionaries. It does not mutate the input, prints an aggregate cleaning report, and optionally updates the supplied reason-count mapping for downstream export.

## Input and output

Input rows use the established eight-field sales schema: `id_venda`, `data_venda`, `cliente`, `produto`, `categoria`, `regiao`, `quantidade`, and `preco_unitario`. Accepted rows retain those fields in the same order and schema. Text fields have surrounding whitespace removed; `id_venda` and `quantidade` are integers; `preco_unitario` is a finite float.

Rows are discarded if any expected schema field is absent; a text field is null; `data_venda` is blank after trimming; `id_venda` cannot be converted to integer; quantity or unit price is missing, blank, or not convertible; or unit price is non-finite. Non-empty dates must be valid calendar dates in `YYYY-MM-DD` format. A rejected row does not stop processing subsequent input rows.

## Reporting and accounting

Prints valid and removed totals plus structured counts for primary rejection reasons: `campo_ausente`, `campo_textual_invalido`, `data_venda_invalida`, `id_venda_invalido`, `quantidade_ausente`, `preco_unitario_ausente`, `quantidade_invalida`, `preco_unitario_invalido`, and `registro_duplicado`. When multiple issues apply, attribute the row once to the earliest reason in validation order: missing fields; text fields (`data_venda`, `cliente`, `produto`, `categoria`, `regiao`); invalid date; quantity; price; identifier (converted after other fields, matching the established record construction order). Exact duplicates are determined by equality of all eight normalized output fields; retain the first occurrence and reject each later copy once. Rows sharing only `id_venda` remain distinct. The function returns only the cleaned list. When supplied, `resumo_remocao` is filled with all reason counters without replacing existing mapping identity. Valid plus removed equals input count; reason counts sum to removed count.

## Edge behavior

An empty input returns an empty cleaned list and reports zero valid and zero removed, with every reason counter at zero. Exact duplicates after normalization retain the first occurrence and count each later copy as `registro_duplicado`. Input dictionaries and their values remain unchanged.
