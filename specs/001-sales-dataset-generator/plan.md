# Implementation Plan: RF01 – Criar ou Carregar o Dataset de Vendas

**Branch**: `001-sales-dataset-generator` | **Date**: 2026-10-26 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-sales-dataset-generator/spec.md`

## Summary

Implementar a rotina de criação determinística e carregamento estruturado do dataset de vendas (`vendas.csv`) dentro do módulo reutilizável `modulo_vendas.py`, utilizando a biblioteca `Faker` (`pt_BR`) combinada com os módulos nativos `csv`, `random` e `pathlib` para gerar no mínimo 100 registros realistas com inconsistências deliberadas controladas (valores nulos, espaços sobressalentes e registro duplicado), além da leitura parametrizada com `csv.DictReader` e tratamento resiliente de falhas de I/O, validados via TDD com `pytest` em `tests/test_modulo_vendas.py`.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: `pandas`, `pytest`, `Faker` (versões fixadas em `requirements.txt`) + biblioteca padrão (`csv`, `random`, `os`, `pathlib`, `datetime`)

**Storage**: Arquivos locais em sistema de arquivos (`vendas.csv` em UTF-8)

**Testing**: `pytest` (`tests/test_modulo_vendas.py`) seguindo ciclo Red-Green-Refactor (TDD)

**Target Platform**: Linux / macOS / Windows e container Docker (Python 3.11+)

**Project Type**: CLI / Data Processing Pipeline Module (`modulo_vendas.py` + `main.py`)

**Performance Goals**: Geração e leitura de 100 a 1.000 registros de vendas em menos de 1 segundo (< 2s limite máximo SC-001)

**Constraints**: Sem caminhos absolutos fixos (hardcoded); leitura obrigatória com `csv.DictReader`; reprodutibilidade 100% determinística via parâmetro `seed`; tratamento seguro de arquivos ausentes sem tracebacks não tratados

**Scale/Scope**: Dataset padrão de 100 a 150 registros com 8 colunas obrigatórias (`id_venda`, `data_venda`, `cliente`, `produto`, `categoria`, `regiao`, `quantidade`, `preco_unitario`)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Princípio da Constituição | Status (Pré-Pesquisa) | Status (Pós-Design) | Evidência / Atendimento |
|---------------------------|-----------------------|---------------------|-------------------------|
| **I. Modularização e Separação de Responsabilidades** | PASS | PASS | `gerar_dataset_sintetico` e `carregar_csv` residem em `modulo_vendas.py` com docstrings e tipagem explícita; `main.py` apenas orquestra a chamada se `vendas.csv` não existir. |
| **II. Processamento Explícito e Estruturas Nativas com Pandas** | PASS | PASS | Uso explícito de `csv.writer`, `csv.DictReader`, listas, dicionários e laços `for`, mantendo `pandas` nas dependências fixadas do projeto. |
| **III. Desenvolvimento Orientado a Testes (TDD - INEGOCIÁVEL)** | PASS | PASS | Testes unitários em `tests/test_modulo_vendas.py` escritos antes da implementação cobrindo geração, determinismo por `seed`, ruídos deliberados, leitura e erro de arquivo inexistente. |
| **IV. Qualidade, Limpeza de Dados e Tratamento Resiliente de Erros** | PASS | PASS | Injeção determinística de nulos, espaços e duplicata para exercitar a limpeza; `carregar_csv` captura `FileNotFoundError`/`OSError` emitindo mensagem clara e retornando `[]`. |
| **V. Padronização de Ambiente com Docker e Rastreabilidade de Saídas** | PASS | PASS | `requirements.txt` com `pandas`, `pytest` e `Faker` com versões fixadas; compatível com execução local e via Docker Compose. |

**Gate Evaluation**: Todos os 5 princípios constitucionais foram atendidos sem violações.

## Project Structure

### Documentation (this feature)

```text
specs/001-sales-dataset-generator/
├── plan.md              # Este arquivo (/speckit.plan)
├── research.md          # Phase 0 output (decisões sobre Faker, csv.DictReader, ruídos e I/O)
├── data-model.md        # Phase 1 output (entidade RegistroVendaBruto e catálogo de referência)
├── quickstart.md        # Phase 1 output (guia de validação e execução do RF01)
├── contracts/           # Phase 1 output
│   └── dataset-contract.md
└── tasks.md             # Phase 2 output (/speckit.tasks - criado na próxima etapa)
```

### Source Code (repository root)

```text
SalesInsight-PY/
├── modulo_vendas.py             # Módulo principal com gerar_dataset_sintetico() e carregar_csv()
├── main.py                      # Ponto de entrada que orquestra a criação/leitura de vendas.csv
├── vendas.csv                   # Dataset de entrada gerado/carregado na raiz do projeto
├── requirements.txt             # Dependências com versões fixadas (pandas, pytest, Faker)
├── Dockerfile                   # Imagem padronizada do projeto
├── docker-compose.yml           # Orquestração de execução e testes
├── README.md                    # Documentação do projeto
├── tests/
│   └── test_modulo_vendas.py    # Suíte de testes unitários automatizados (pytest)
└── outputs/                     # Diretório de artefatos gerados pelo pipeline completo
```

**Structure Decision**: Estrutura enxuta na raiz do repositório conforme exigido pela Constituição (`Stack Tecnológica e Restrições Arquiteturais`) e pela seção `4.1. ORGANIZAÇÃO DO PROJETO` de `ASSIGMENT.md` (`modulo_vendas.py`, `main.py`, `vendas.csv`, `tests/test_modulo_vendas.py`, `outputs/`).

## Complexity Tracking

Nenhuma violação da Constituição. Tabela não aplicável.
