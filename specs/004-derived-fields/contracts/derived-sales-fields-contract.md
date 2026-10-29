# Contrato: Campos Derivados de Vendas

## Função de domínio

`criar_campos_derivados(dados)` recebe uma lista ordenada de registros de venda limpos e retorna lista com os mesmos registros, agora contendo `receita_total` e `faixa_preco`.

## Pré-condições

- Cada registro contém `quantidade` e `preco_unitario` válidos, conforme etapa de limpeza.

## Pós-condições

- `receita_total` é o produto arredondado a duas casas decimais.
- `faixa_preco` é `Baixo` para receita < 500, `Médio` para receita de 500 até 2.000 inclusive, e `Alto` para receita > 2.000.
- Campos restantes, cardinalidade e ordem permanecem iguais.
- Entrada vazia retorna lista vazia.

## Falhas

Tratamento de entradas inválidas fora do contrato não faz parte desta feature; limpeza anterior é responsável por validar os campos obrigatórios.
