# Modelo de Dados: Segmentação de Clientes por Gasto

## Compra de venda

Registro validado e enriquecido pelo pipeline, com um cliente identificado e receita total de uma compra.

| Campo | Tipo conceitual | Regra |
|---|---|---|
| `cliente` | Identificador textual | Valor não vazio, normalizado na etapa de limpeza; agrupa compras do mesmo cliente. |
| `receita_total` | Valor monetário decimal | Receita da compra já calculada e arredondada a duas casas na etapa de campos derivados. |

## Cliente segmentado

Uma saída por cliente distinto presente nas compras recebidas.

| Campo | Tipo conceitual | Regra |
|---|---|---|
| `total_gasto` | Valor monetário decimal | Soma das receitas das compras do cliente, exibida arredondada a duas casas. |
| `segmento` | Categoria enumerada | `Bronze` se total < R$ 3.000; `Prata` se R$ 3.000 <= total <= R$ 8.000; `Ouro` se total > R$ 8.000. |

## Relações e transformação

Cada compra pertence a exatamente um cliente; um cliente pode possuir zero ou mais compras. Compras do mesmo cliente são agrupadas, sem misturar clientes. A classificação usa o total acumulado antes do arredondamento de apresentação. Entrada vazia produz mapa sem clientes; cliente com compra válida produz exatamente uma saída.
