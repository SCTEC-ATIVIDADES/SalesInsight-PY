# Research: RF06 – Segmentar Clientes por Nível de Gasto

## Decisões

### Acumular receitas do cliente por venda
- **Decision**: Agrupar `receita_total` pela identidade `cliente`, somando os valores de cada venda antes de classificar.
- **Rationale**: A regra exige gasto acumulado, e registros derivados já contêm receita por venda arredondada a centavos.
- **Alternatives considered**: Classificar cada venda e depois combinar categorias; rejeitada porque não calcula gasto acumulado por cliente.

### Precisão financeira
- **Decision**: Converter cada `receita_total` validada para `Decimal` a partir de sua representação decimal e somar sem arredondamentos intermediários; arredondar o total exposto a duas casas decimais. Classificar pelo gasto acumulado não arredondado.
- **Rationale**: Evita artefatos binários no limite dos segmentos e respeita o total efetivo dos valores em centavos. A etapa RF04 já arredonda receita por compra.
- **Alternatives considered**: Somar floats; rejeitada por imprecisão potencial. Arredondar acumulado após cada venda; rejeitada por alterar a soma dependendo da ordem.

### Limites de segmentação
- **Decision**: Bronze para total < 3000; Prata para 3000 <= total <= 8000; Ouro para total > 8000.
- **Rationale**: Interpretação literal da tabela e do exemplo fornecidos, incluindo ambos os limites no intervalo Prata.
- **Alternatives considered**: Limites arredondados antes da classificação; rejeitada pois pode classificar incorretamente valores acumulados que difiram por frações de centavo.

### Integração
- **Decision**: Colocar função reutilizável em `modulo_vendas.py`, chamar em `main.py` e incluir saída no mapa existente de métricas exportado pelo CSV/JSON genérico.
- **Rationale**: Segue arquitetura RF05 e constituição, preservando envelopes/formato atual.
- **Alternatives considered**: Novo módulo ou novos formatos de arquivo; rejeitados por duplicação e expansão desnecessária de interface.

## Evidências do projeto

- `modulo_vendas.limpar_dados` valida e normaliza `cliente`; `criar_campos_derivados` gera `receita_total` arredondada a duas casas.
- `main.py` executa limpeza, deriva campos, monta métricas e chama `exportar_resultados`.
- `exportar_resultados` aceita o mapa de métricas existente e o serializa sob `metricas_gerais` em JSON e como linhas `Métrica, Valor` em CSV.
- `tests/test_modulo_vendas.py` é suíte pytest central; convenções RF05 cobrem pipeline e exportações.

## Clarificações

Nenhuma pendente. Entrada assumida válida segundo o pipeline anterior.
