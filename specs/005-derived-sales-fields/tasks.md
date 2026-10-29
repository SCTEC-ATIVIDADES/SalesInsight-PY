# Tasks: RF04 – Criar Campos Derivados

**Input**: Design documents from `/specs/005-derived-sales-fields/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: TDD obrigatório conforme constituição; escrever testes antes da implementação e confirmar falha inicial.

## Phase 1: Setup

Nenhuma configuração ou dependência nova necessária.

## Phase 2: Foundational

Nenhuma tarefa fundacional; estrutura e etapa de limpeza já existem.

## Phase 3: User Story 1 - Calcular receita por registro (Priority: P1) — MVP

**Goal**: Adicionar receita total arredondada a cada registro, mantendo dados existentes.

**Independent Test**: Executar testes focados para registros simples/múltiplos; confirmar receita arredondada, preservação dos demais campos e ordem.

### Tests

- [ ] T001 [US1] Adicionar testes de receita arredondada, campos preservados e ordem em `tests/test_modulo_vendas.py`; executar para confirmar falha antes da implementação.

### Implementation

- [ ] T002 [US1] Implementar `criar_campos_derivados(dados)` com cálculo `round(quantidade * preco_unitario, 2)` e retorno dos registros em `modulo_vendas.py`.

**Checkpoint**: US1 funciona e testes de receita passam independentemente.

## Phase 4: User Story 2 - Classificar registros por faixa de receita (Priority: P2)

**Goal**: Classificar cada registro pela receita total: Baixo (< 500), Médio (500–2.000 inclusive), Alto (> 2.000).

**Independent Test**: Testar valores abaixo, exatamente em e acima dos limites; confirmar faixa atribuída a partir da receita arredondada.

### Tests

- [ ] T003 [US2] Adicionar testes de classificação para receita abaixo de 500, igual a 500, igual a 2.000 e acima de 2.000 em `tests/test_modulo_vendas.py`; executar para confirmar falha antes da implementação da classificação.

### Implementation

- [ ] T004 [US2] Completar `criar_campos_derivados` atribuindo `faixa_preco` conforme os limites inclusivos definidos, usando `receita_total` arredondada, em `modulo_vendas.py`.

**Checkpoint**: US1 e US2 funcionam; testes de receita e limites passam.

## Phase 5: Polish & Cross-Cutting Concerns

- [ ] T005 [P] Executar validação quickstart (`pytest tests/test_modulo_vendas.py`, `pytest` e `python main.py`) conforme `specs/005-derived-sales-fields/quickstart.md`.

## Dependencies & Execution Order

### Phase Dependencies

- Setup e Foundational: sem tarefas; nada bloqueia início.
- US1: independente; entregar primeiro como MVP.
- US2: depende de T002, pois classificação consome `receita_total` calculada.
- Polish: depende de T002 e T004.

### User Story Dependencies

- **US1 (P1)**: sem dependências; T001 → T002.
- **US2 (P2)**: após US1; T003 → T004 e depende de T002.

### Parallel Opportunities

- T001 e T003 compartilham `tests/test_modulo_vendas.py`; não paralelizar.
- T002 e T004 compartilham `modulo_vendas.py` e têm dependência funcional; executar em sequência.
- T005 roda após ambas as histórias; sem paralelismo útil neste escopo pequeno.

## Implementation Strategy

### MVP First

1. Fazer T001 e confirmar teste falhando.
2. Fazer T002 e validar US1 isoladamente.
3. Para classificação, fazer T003 (teste falha) e T004.
4. Executar T005 antes de concluir.

### Incremental Delivery

US1 entrega receita calculada. US2 acrescenta faixa ao mesmo processamento, reutilizando a receita calculada e sem duplicar transformação.

## Notes

- [P] indica tarefas paralelizáveis em arquivos distintos, sem dependência pendente.
- Reter função no módulo existente; nenhuma dependência nova.
- Não alterar dados fora do escopo da feature.
