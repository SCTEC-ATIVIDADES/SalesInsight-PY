# Pesquisa: Campos Derivados de Vendas

## Decisão: Cálculo escalar explícito em uma passagem

**Decision**: Calcular produto de quantidade por preço unitário em cada registro, arredondar para duas casas e atribuir faixa usando o valor arredondado.

**Rationale**: Correspondente à regra e ao exemplo da especificação; preserva processamento explícito exigido pela constituição, com custo linear e sem dependência nova.

**Alternatives considered**: Vetorização pandas; descartada por adicionar complexidade para cálculo simples por registro.

## Decisão: Integrar à função existente no pipeline

**Decision**: Manter transformação reutilizável em `modulo_vendas.py`; orquestração fica em `main.py` e testes em `tests/test_modulo_vendas.py`.

**Rationale**: Alinha-se à arquitetura existente e à constituição; limpeza prévia já valida campos de entrada.

**Alternatives considered**: Novo módulo ou camada de serviço; desnecessários para uma transformação pequena e interna.

## Decisão: Regras de limite inclusivas e ordem mantida

**Decision**: Classificar `< 500` como Baixo, `500 <= receita <= 2000` como Médio, e `> 2000` como Alto; classificar após arredondamento; preservar demais campos e ordem.

**Rationale**: Resolve explicitamente limites e precisão conforme requisitos RF04.

**Alternatives considered**: Classificar produto não arredondado; descartada porque pode produzir faixa incompatível com valor `receita_total` exibido.
