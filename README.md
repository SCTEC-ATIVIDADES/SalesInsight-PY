# SalesInsight PY

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat-square&logo=docker)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

Pipeline completo de ciência de dados em Python para geração, ingestão, limpeza e análise de dados de vendas.

## Arquitetura do Projeto

- `gerador_dados.py`: Módulo independente responsável pela geração determinística do dataset sintético (`gerar_dataset_sintetico`) com dados realistas em português (`Faker('pt_BR')` + `random`) e ruídos controlados para validação de limpeza.
- `modulo_vendas.py`: Módulo de funções reutilizáveis do pipeline de vendas (`carregar_csv` via `csv.DictReader` e `inspecionar_dados` para diagnóstico estrutural e contagem de registros incompletos/nulos).
- `main.py`: Ponto de entrada e orquestrador do pipeline (`gerar_dataset_sintetico` -> `carregar_csv` -> `inspecionar_dados`).
- `vendas.csv`: Dataset de vendas gerado com `>= 100` registros (150 registros base + 1 duplicata deliberada = 151 linhas de dados).
- `tests/test_modulo_vendas.py`: Suíte automatizada de testes unitários com `pytest`.


## Segmentação de clientes por gasto

O pipeline soma `receita_total` por cliente e classifica: Bronze abaixo de R$ 3.000; Prata de R$ 3.000 a R$ 8.000, inclusive; Ouro acima de R$ 8.000. Totais e segmentos aparecem nos relatórios CSV e JSON existentes.

## Conceitos e decisões

O pipeline lê CSV com `csv.DictReader`, mantendo cabeçalhos como chaves e cada venda como dicionário. A segmentação usa agregação explícita por cliente e valores `Decimal`, classificando o total antes do arredondamento de exibição.

## Testes e limitações

Desenvolvimento segue TDD: escrever teste, confirmar falha, implementar e refatorar; suíte fica em `tests/test_modulo_vendas.py`. Segmentação pressupõe dados previamente limpos, com `cliente` válido e `receita_total` finita; rejeição de dados ocorre na limpeza anterior. Execute localmente com `pytest -v` ou via Compose com `docker compose run --rm app pytest -v`.

## Saídas

`outputs/estatisticas.json` mantém envelope `metricas_gerais`; `outputs/metricas_resumo.csv` mantém colunas `Métrica, Valor`. Ambos incluem `segmentacao_clientes` junto das métricas existentes.

## Execução com Docker Compose (Recomendado)

### Executar o pipeline principal

```bash
docker compose up --build
```

### Executar a suíte de testes (`pytest`)

```bash
docker compose run --rm app pytest -v
```

## Execução Local com Ambiente Virtual (`venv`)

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS (No Windows: .venv\Scripts\activate)
pip install -r requirements.txt
python main.py
pytest -v
```
