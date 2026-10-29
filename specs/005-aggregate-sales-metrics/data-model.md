# Data Model: Aggregated Sales Metrics

## Input: Sales record

Each input record is already cleaned and enriched by RF04.

| Field | Conceptual type | Rule |
|---|---|---|
| `categoria` | Text | Category key used as received; no extra normalization. |
| `regiao` | Text | Region key used as received; no extra normalization. |
| `receita_total` | Decimal number | Finite revenue already rounded to two decimal places per sale. |

## Output: Aggregated metrics

| Field | Conceptual type | Rule |
|---|---|---|
| `total_geral` | Decimal number | Sum of all `receita_total` values, rounded to two decimals at the end. |
| `por_categoria` | Dictionary of text to decimal | One total per category; round accumulator to two decimals after each addition. |
| `por_regiao` | Dictionary of text to decimal | One total per region; round accumulator to two decimals after each addition. |

Each input record contributes once to its category, region, and general total. Empty input produces `0.0`, `{}`, and `{}` respectively.
