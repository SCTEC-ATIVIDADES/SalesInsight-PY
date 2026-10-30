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
