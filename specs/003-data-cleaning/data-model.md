# Data Model: RF03 – Limpar e Tratar os Dados

## Raw sales record

Represents one row received from the existing CSV-loading stage.

| Field | Input form | Validation / handling |
|---|---|---|
| `id_venda` | Text identifier | Convert to integer for accepted output; conversion failure rejects the row. |
| `data_venda` | Text date | Required, non-null, nonblank after trimming, and valid in `YYYY-MM-DD` format; retain as text. |
| `cliente` | Text | Required and non-null; trim surrounding whitespace. |
| `produto` | Text | Required and non-null; trim surrounding whitespace. |
| `categoria` | Text | Required and non-null; trim surrounding whitespace. |
| `regiao` | Text | Required and non-null; trim surrounding whitespace. |
| `quantidade` | Text or missing/null | Required; trimmed value must convert to integer. |
| `preco_unitario` | Text or missing/null | Required; trimmed value must convert to finite decimal-number representation. |

## Clean sales record

A newly constructed record retaining the eight fields above in their established schema and input order. Text fields are stripped; `id_venda` and `quantidade` are integers; `preco_unitario` is a finite float. Accepted records do not mutate the corresponding raw record.

## Cleaning report

- `validos`: number of accepted records.
- `removidos`: number of rejected input records; each rejected row contributes exactly one.
- `motivos_remocao`: structured counts attributed to one primary reason per rejected row, printed with the cleaning summary: `campo_ausente`, `campo_textual_invalido`, `data_venda_invalida`, `id_venda_invalido`, `quantidade_ausente`, `preco_unitario_ausente`, `quantidade_invalida`, `preco_unitario_invalido`, or `registro_duplicado`.
- Invariant: `validos + removidos == total de entradas`; reason counts sum to `removidos`.

## Relationships and lifecycle

Each raw record is evaluated once and results in exactly one clean record or one rejection entry. Exact duplicate normalized records retain the first occurrence; later copies are rejected as `registro_duplicado`. The report summarizes this transformation. An empty input yields empty output and zero counts for every reason. Dates must be valid `YYYY-MM-DD` calendar dates, and unit price must be finite.
