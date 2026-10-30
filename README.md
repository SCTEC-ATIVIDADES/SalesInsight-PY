# SalesInsight PY

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat-square&logo=docker)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

Pipeline completo de ciência de dados em Python para geração, ingestão, limpeza e análise de dados de vendas.

## Arquitetura do Projeto

- `gerador_dados.py`: Módulo independente responsável pela geração determinística do dataset sintético (`gerar_dataset_sintetico`) com dados realistas em português (`Faker('pt_BR')` + `random`) e ruídos controlados para validação de limpeza.
- `modulo_vendas.py`: Funções reutilizáveis do pipeline (`carregar_csv` via `csv.DictReader`, inspeção, limpeza, transformações, métricas, segmentação e exportação via módulos nativos `csv`/`json`).
- `main.py`: Ponto de entrada que orquestra geração, leitura, processamento e exportação, sem regras de negócio. Importá-lo não inicia pipeline; execução direta exibe receita total e até cinco clientes de maior gasto.
- `vendas.csv`: Dataset de vendas gerado com `>= 100` registros (150 registros base + 1 duplicata deliberada = 151 linhas de dados).
- `tests/test_modulo_vendas.py`: Suíte automatizada de testes unitários com `pytest`.


## Segmentação de clientes por gasto

O pipeline soma `receita_total` por cliente e classifica: Bronze abaixo de R$ 3.000; Prata de R$ 3.000 a R$ 8.000, inclusive; Ouro acima de R$ 8.000. Totais e segmentos aparecem na chave `clientes` do JSON; o CSV resume somente receita por categoria.

## Conceitos e decisões

O pipeline lê CSV com `csv.DictReader`, mantendo cabeçalhos como chaves e cada venda como dicionário. Usa módulos nativos `csv` e `json` para I/O; valores permanecem strings na leitura e conversão/validação ocorrem nas etapas de limpeza. CSV foi escolhido por ser formato tabular simples, legível e interoperável. A segmentação agrega por cliente usando `Decimal`.

## Saídas

`outputs/estatisticas.json` contém chaves de topo `metricas_gerais` e `clientes`. `outputs/metricas_resumo.csv` contém cabeçalho `Categoria, Receita Total` e uma linha por item de `metricas_gerais.por_categoria`. Arquivos usam UTF-8; pasta `outputs/` é criada automaticamente e exportação substitui arquivos existentes.

## Instalação e execução local

Requisitos: Python 3.11+. Instale dependências fixadas e rode pipeline/testes:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
pytest -q
```

## Testes e limitações

Desenvolvimento segue TDD: escrever teste, confirmar falha, implementar, confirmar sucesso e refatorar; suíte fica em `tests/test_modulo_vendas.py`. Segmentação pressupõe dados previamente limpos, com `cliente` válido e `receita_total` finita; limpeza/rejeição de dados ocorre antes da exportação.

## Execução com Docker Compose (Recomendado)

Requisitos: Docker Engine instalado e Docker Compose v2 (`docker compose`) disponível.

### Executar a suíte e pipeline (`pytest` + `main.py`)

```bash
docker compose run --build --rm app pytest -v
docker compose run --rm app python main.py
```

## Ativação do ambiente virtual no Windows

Use `.venv\\Scripts\\activate`.
