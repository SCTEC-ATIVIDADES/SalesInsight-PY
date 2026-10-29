# Implementation Plan: RF02 – Inspecionar e Descrever os Dados

**Branch**: `002-data-inspection` | **Date**: 2026-10-28 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-data-inspection/spec.md`

## Summary

Implementar a função `inspecionar_dados(dados)` em `modulo_vendas.py` e integrá-la ao fluxo principal em `main.py` para exibir o diagnóstico inicial dos registros brutos carregados (cabeçalho de inspeção, quantidade total de registros, lista de campos disponíveis, exemplo do primeiro registro e verificação explícita de linhas com dados incompletos ou nulos), mantendo os dados originais intactos e retornando um resumo estruturado determinístico validado via TDD com `pytest` em `tests/test_modulo_vendas.py`.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: `pandas`, `pytest`, `Faker` (versões fixadas em `requirements.txt`) + biblioteca padrão (`csv`, `os`, `typing`)

**Storage**: N/A (opera em memória sobre a lista de dicionários carregada de `vendas.csv`)

**Testing**: `pytest` (`tests/test_modulo_vendas.py`) seguindo ciclo Red-Green-Refactor (TDD)

**Target Platform**: Linux / macOS / Windows via ambiente virtual isolado (`.venv`) e container Docker (Python 3.11+)

**Project Type**: CLI / Data Processing Pipeline Module (`modulo_vendas.py` + `main.py`)

**Performance Goals**: Inspeção completa de até 10.000 registros em menos de 1 segundo (SC-001)

**Constraints**: Processamento explícito e legível com listas, dicionários, laços `for` e condicionais; operação 100% somente-leitura sem mutação da lista de entrada; tratamento seguro para lista vazia (`[]`) sem `IndexError`

**Scale/Scope**: Dataset padrão de 100 a 151 registros brutos com 8 colunas (`id_venda`, `data_venda`, `cliente`, `produto`, `categoria`, `regiao`, `quantidade`, `preco_unitario`)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Princípio da Constituição | Status (Pré-Pesquisa) | Status (Pós-Design) | Evidência / Atendimento |
|---------------------------|-----------------------|---------------------|-------------------------|
| **I. Modularização e Separação de Responsabilidades** | PASS | PASS | `inspecionar_dados` reside em `modulo_vendas.py` com docstring concisa e tipagem explícita de parâmetros e retorno; `main.py` apenas invoca `mv.inspecionar_dados(dados_brutos)` dentro do bloco `if __name__ == "__main__":`. |
| **II. Processamento Explícito e Estruturas Nativas com Pandas** | PASS | PASS | Verificação de linhas incompletas/nulas implementada com laços `for` e estruturas condicionais explícitas sobre a lista de dicionários, preservando clareza didática e auditabilidade. |
| **III. Desenvolvimento Orientado a Testes (TDD - INEGOCIÁVEL)** | PASS | PASS | Testes unitários em `tests/test_modulo_vendas.py` escritos antes da implementação cobrindo saída padrão (`capsys`), contagem de linhas incompletas/nulas, coleção vazia (`[]`) e imutabilidade dos dados de entrada. |
| **IV. Qualidade, Limpeza de Dados e Tratamento Resiliente de Erros** | PASS | PASS | Identifica de forma determinística valores `None`, strings vazias (`""`) e strings compostas apenas por espaços (`"   "`), tratando coleções vazias sem levantar exceções. |
| **V. Padronização de Ambiente com Docker e Rastreabilidade de Saídas** | PASS | PASS | Nenhuma nova dependência externa necessária; compatível integralmente com `.venv` e `docker compose`. |

**Gate Evaluation**: Todos os 5 princípios constitucionais atendidos sem violações.

## Project Structure

### Documentation (this feature)

```text
specs/002-data-inspection/
├── plan.md              # Este arquivo (/speckit.plan)
├── research.md          # Phase 0 output (decisões sobre formato de saída, detecção de nulos e contrato de retorno)
├── data-model.md        # Phase 1 output (entidades RegistroVendaBruto e ResumoInspecaoDados)
├── quickstart.md        # Phase 1 output (guia de validação e execução do RF02)
├── contracts/           # Phase 1 output
│   └── inspection-contract.md
└── tasks.md             # Phase 2 output (/speckit.tasks - criado na próxima etapa)
```

### Source Code (repository root)

```text
SalesInsight-PY/
├── gerador_dados.py             # Módulo independente dedicado à geração do dataset (RF01)
├── modulo_vendas.py             # Módulo principal do pipeline (carregar_csv, inspecionar_dados)
├── main.py                      # Ponto de entrada que orquestra geração, leitura e inspeção (RF01-RF02)
├── vendas.csv                   # Dataset de entrada gerado/carregado na raiz do projeto
├── requirements.txt             # Dependências com versões fixadas (pandas, pytest, Faker)
├── Dockerfile                   # Imagem padronizada do projeto
├── docker-compose.yml           # Orquestração de execução e testes
├── tests/
│   └── test_modulo_vendas.py    # Suíte de testes unitários automatizados (pytest)
└── outputs/                     # Diretório de artefatos gerados pelo pipeline completo
```

**Structure Decision**: Manter a arquitetura enxuta na raiz do repositório conforme a Constituição, adicionando `inspecionar_dados` diretamente em `modulo_vendas.py`, atualizando a orquestração em `main.py` e expandindo a suíte `tests/test_modulo_vendas.py`.

## Complexity Tracking

Nenhuma violação da Constituição. Tabela não aplicável.
