# Modelo de Dados: Campos Derivados

## Registro de venda

Registro já validado pela etapa de limpeza, contendo ao menos `quantidade` e `preco_unitario`; os demais campos de venda permanecem inalterados.

| Campo | Tipo conceitual | Regra |
|---|---|---|
| `quantidade` | Inteiro | Valor validado na etapa de limpeza. |
| `preco_unitario` | Número decimal | Valor finito validado na etapa de limpeza. |
| `receita_total` | Número decimal | `quantidade × preco_unitario`, arredondado a duas casas decimais. |
| `faixa_preco` | Texto enumerado | `Baixo` se receita < 500; `Médio` se 500 ≤ receita ≤ 2000; `Alto` se receita > 2000. |

## Relações e transformação

Cada registro de entrada corresponde a um registro de saída; cardinalidade, ordem e campos originais são preservados. A classificação usa `receita_total` já arredondada. Lista vazia permanece vazia.
