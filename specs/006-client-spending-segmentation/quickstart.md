# Quickstart: Validar Segmentação de Clientes

## Pré-requisitos

- Python 3.11+ e dependências do projeto instaladas no ambiente virtual (`.venv`).
- Repositório na raiz do projeto.

## Validação automatizada

Execute suíte relacionada ao módulo de vendas:

```sh
.venv/bin/python -m pytest tests/test_modulo_vendas.py
```

Resultado esperado: testes passam incluindo gasto agregado por cliente, limites R$ 3.000/R$ 8.000, entrada vazia e integração com pipeline/exportação.

## Validação ponta a ponta

Execute pipeline no ambiente do projeto:

```sh
.venv/bin/python main.py
```

Resultado esperado: fluxo valida e enriquece vendas, calcula métricas e inclui mapa de segmentação de clientes nos arquivos `outputs/estatisticas.json` e `outputs/metricas_resumo.csv`. JSON mantém envelope `metricas_gerais`; CSV mantém cabeçalho `Métrica, Valor`.

## Validação via Docker Compose

```sh
docker compose run --rm app pytest -v
docker compose up --build
```

Resultado esperado: suíte passa e pipeline gera ambos os relatórios com segmentação, sem erro.

Para cenário controlado, fornecer ao pipeline vendas válidas cujos totais por cliente sejam abaixo de R$ 3.000, exatamente R$ 3.000, exatamente R$ 8.000 e acima de R$ 8.000. Resultado esperado: respectivamente `Bronze`, `Prata`, `Prata` e `Ouro`; compras repetidas do mesmo cliente devem ser somadas antes da classificação.

Modelo de campos: [data-model.md](./data-model.md). Critérios completos: [spec.md](./spec.md).
