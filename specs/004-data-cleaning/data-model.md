# Data Model: RF03 – Limpar e Tratar os Dados

## Raw sales record

Represents one row received from the existing CSV-loading stage.

| Field | Input form | Validation / handling |
|---|---|---|
| `id_venda` | Text identifier | Convert to integer for accepted output; conversion failure rejects the row. |
| `data_venda` | Text date | Trim surrounding whitespace; retain as text. |
| `cliente` | Text | Trim surrounding whitespace. |
| `produto` | Text | Trim surrounding whitespace. |
| `categoria` | Text | Trim surrounding whitespace. |
| `regiao` | Text | Trim surrounding whitespace. |
| `quantidade` | Text or missing/null | Required; trimmed value must convert to integer. |
| `preco_unitario` | Text or missing/null | Required; trimmed value must convert to finite decimal-number representation. |

## Clean sales record

A newly constructed record retaining the eight fields above in their established schema and input order. Text fields are stripped; `id_venda` and `quantidade` are integers; `preco_unitario` is a finite float. Accepted records do not mutate the corresponding raw record.

## Cleaning report

- `validos`: number of accepted records.
- `removidos`: number of rejected input records; each rejected row contributes exactly one.
- `motivos_remocao`: structured counts attributed to a primary reason, reported with the cleaning summary: `quantidade_ausente`, `preco_unitario_ausente`, `quantidade_invalida`, `preco_unitario_invalido`, or `id_venda_invalido`.
- Invariant: `validos + removidos == total de entradas`; reason counts sum to `removidos`.

## Relationships and lifecycle

Each raw record is evaluated once and results in exactly one clean record or one rejection entry. The report summarizes this transformation. An empty input yields empty output and zero counts.
