# Implementation Plan: RF04 – Criar Campos Derivados

**Branch**: `005-derived-sales-fields` | **Date**: 2026-10-29 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/005-derived-sales-fields/spec.md`

## Summary

Adicionar em `modulo_vendas.py` uma transformação reutilizável que calcula `receita_total` arredondada a duas casas e classifica cada venda em `faixa_preco`, preservando registros e ordem. Cobrir limites, precisão, lista vazia e preservação com testes pytest em `tests/test_modulo_vendas.py`, seguindo TDD; sem dependências novas.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: pandas 2.2.3 e pytest 8.3.4 já fixados; lógica da transformação usa estruturas nativas, sem dependência nova.

**Storage**: N/A; transformação em memória sobre lista de dicionários já limpa.

**Testing**: `pytest` em `tests/test_modulo_vendas.py`, com ciclo TDD obrigatório.

**Target Platform**: Linux / macOS / Windows via Python 3.11+, `.venv` e Docker existente.

**Project Type**: Pipeline CLI de processamento de vendas (`modulo_vendas.py` + `main.py`).

**Performance Goals**: Uma passagem linear pela coleção; processar até 10.000 registros em tempo adequado para execução local.

**Constraints**: Quantidade e preço unitário já validados pela limpeza; calcular e arredondar receita antes da classificação; manter campos e ordem recebidos; limiares exatos: abaixo de 500, 500–2.000 inclusive, acima de 2.000.

**Scale/Scope**: Uma função reutilizável no módulo existente e testes correspondentes; sem alterações de esquema de entrada, armazenamento ou dependências.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Princípio | Pré-Pesquisa | Pós-Design | Evidência |
|---|---|---|---|
| I. Modularização e Separação de Responsabilidades | PASS | PASS | Transformação fica em `modulo_vendas.py`; `main.py` continua orquestrador. |
| II. Processamento Explícito e Estruturas Nativas com Pandas | PASS | PASS | Laço, dicionários e condicionais explícitos; pandas não é necessário para cálculo escalar. |
| III. Desenvolvimento Orientado a Testes (TDD) | PASS | PASS | Testes pytest em `tests/test_modulo_vendas.py` precedem implementação e cobrem valores e fronteiras. |
| IV. Qualidade, Limpeza e Tratamento Resiliente | PASS | PASS | Escopo assume entrada limpa conforme spec; classificação determinística após arredondamento. |
| V. Ambiente Padronizado e Rastreabilidade | PASS | PASS | Dependências e ambiente existentes; validação usa pytest, `python main.py` e Docker Compose conforme gates do projeto. |

**Gate Evaluation**: Nenhuma violação identificada. A especificação limita a entrada a registros previamente limpos; cálculos e fronteiras têm resultados determinísticos e testáveis.

## Project Structure

### Documentation (this feature)

```text
specs/005-derived-sales-fields/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── derived-sales-fields-contract.md
└── tasks.md
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

**Structure Decision**: Manter layout existente. Implementação e teste pertencem ao módulo e suíte já existentes; contrato documenta a função pública interna do pipeline, sem criar API externa ou arquivo de código.

## Complexity Tracking

Nenhuma violação constitucional; sem abstrações, dependências ou módulos adicionais.
