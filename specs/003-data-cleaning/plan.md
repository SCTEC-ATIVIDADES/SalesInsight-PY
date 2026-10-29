# Implementation Plan: RF03 – Limpar e Tratar os Dados

**Branch**: `003-data-cleaning` | **Date**: 2026-10-29 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/003-data-cleaning/spec.md`

## Summary

Implementar `limpar_dados` como função reutilizável em `modulo_vendas.py`: criar registros sem alterar a entrada, normalizar espaços textuais, converter identificador/quantidade/preço, rejeitar linhas com quantidade ou preço ausente/inválido, contabilizar válidos e removidos, e testar em `tests/test_modulo_vendas.py` seguindo TDD com `pytest`.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Biblioteca padrão do Python e `pytest` já presente no projeto; nenhuma dependência nova.

**Storage**: N/A; transformação em memória sobre lista de dicionários carregada de `vendas.csv`.

**Testing**: `pytest` em `tests/test_modulo_vendas.py`, conforme ciclo TDD da constituição.

**Target Platform**: Linux / macOS / Windows via Python 3.11+, ambiente `.venv` e Docker existente.

**Project Type**: Módulo de processamento de dados em pipeline CLI (`modulo_vendas.py` + `main.py`).

**Performance Goals**: Processar o dataset de escopo (até 10.000 linhas) linearmente em tempo adequado a execução local; o plano não introduz meta de latência nova para esta transformação. A funcionalidade de limpeza não exige infraestrutura adicional de load testing.

**Constraints**: Lógica explícita com listas, dicionários, laços e condicionais; não mutar entrada; linha malformada ou ausência/invalidade de campos obrigatórios deve ser rejeitada uma única vez e sem interromper o lote; datas seguem formato `YYYY-MM-DD`; preços devem ser finitos.

**Scale/Scope**: Dataset padrão de 100 a 151 linhas e oito campos; mudança circunscrita à limpeza e seus testes, sem alterar leitura ou geração.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Princípio da Constituição | Status (Pré-Pesquisa) | Status (Pós-Design) | Evidência / Atendimento |
|---------------------------|-----------------------|---------------------|-------------------------|
| I. Modularização e Separação de Responsabilidades | PASS | PASS | Lógica isolada em `modulo_vendas.py`; `main.py` permanece orquestrador; função com docstring, tipagem de entrada e retorno explícitas. |
| II. Processamento Explícito e Estruturas Nativas com Pandas | PASS | PASS | Transformação implementável por laço explícito sobre listas e dicionários; sem abstrações opacas nem nova biblioteca. |
| III. Desenvolvimento Orientado a Testes (TDD) | PASS | PASS | Testes em `tests/test_modulo_vendas.py` devem preceder implementação e cobrir válidos, valores ausentes/brancos/inválidos, contagens, ordem, entrada imutável e lista vazia. |
| IV. Qualidade, Limpeza e Tratamento Resiliente | PASS | PASS | Ausências, valores inválidos, linhas malformadas e cópias exatas após normalização são rejeitadas deterministicamente; relatório imprime contagens estruturadas por motivo, com atribuição única por linha e totais reconciliáveis. Registros distintos com mesmo ID permanecem válidos. |
| V. Ambiente Padronizado e Rastreabilidade | PASS | PASS | Nenhuma dependência nova para RF03; `.venv` e Docker Compose executam a suíte e `main.py`. T009–T011 verificaram todos os quality gates e a geração dos dois artefatos em `outputs/`. |

**Gate Evaluation**: Os cinco princípios foram verificados. Testes passaram via pytest local e Docker Compose; `main.py` gerou `outputs/metricas_resumo.csv` e `outputs/estatisticas.json` localmente e via Docker. Cópias exatas após normalização são removidas deterministicamente, mantendo a primeira ocorrência e contabilizando `registro_duplicado`; registros distintos com mesmo ID são preservados. A função retorna somente a lista limpa; totais e contadores estruturados por motivo são apresentados no relatório impresso e disponibilizados para exportação.
## Project Structure

### Documentation (this feature)

```text
specs/003-data-cleaning/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── cleaning-contract.md
└── tasks.md              # Generated later by /speckit.tasks
```

### Source Code (repository root)

```text
SalesInsight-PY/
├── modulo_vendas.py
├── main.py
├── gerador_dados.py
├── requirements.txt
└── tests/
    └── test_modulo_vendas.py
```

**Structure Decision**: Keep the existing root-level CLI/data-processing module layout. Add `limpar_dados` to `modulo_vendas.py` and expand the existing pytest module; no new source modules or dependencies are needed.

## Complexity Tracking

No constitution violations; no additional projects, abstractions, or dependencies are required.
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
