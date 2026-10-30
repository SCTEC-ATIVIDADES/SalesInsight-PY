# Data Model: RF08 Pipeline Entry Point

RF08 introduces no persistent entity or schema. It orchestrates existing sales records and computed results.

## Sales record

- Source: `vendas.csv`, read by existing `carregar_csv`.
- Fields: Existing CSV headers and row values; raw values are strings until cleaning/transformations.
- Invariants: Existing cleanup rejects invalid/incomplete/duplicate records and tracks removal reasons.

## Pipeline metrics

- Produced by: Existing metrics calculation plus orchestration counts (`registros_validos`, `registros_removidos`, `motivos_remocao`).
- Fields: `total_geral`, `por_categoria`, `por_regiao`, and processing counts.
- Invariants: Totals derive from cleaned, transformed records; monetary values follow established RF05/RF07 behavior.

## Customer segmentation

- Produced by: `segmentar_clientes_por_gasto` from transformed sales.
- Shape: Customer name mapped to `total_gasto` and `segmento`.
- Invariants: Existing RF06 thresholds remain authoritative: Bronze below R$3,000; Prata R$3,000–R$8,000 inclusive; Ouro above R$8,000. Top-five display is derived from these results and does not alter exported data.

## Exported outputs

- JSON: `outputs/estatisticas.json`, top-level keys `metricas_gerais` and `clientes`.
- CSV: `outputs/metricas_resumo.csv`, columns `Categoria, Receita Total` and one row per category total.
- These schemas are defined by RF07 and are not changed by RF08.
