# Feature Specification: RF05 – Calcular Métricas Agregadas

**Feature Branch**: `005-aggregate-sales-metrics`

**Created**: 2026-10-29

**Status**: Draft

**Input**: User description: "RF05 – Calcular Métricas Agregadas. Desenvolver funções agregadoras utilizando dicionários para calcular receita total por Categoria, receita total por Região e total geral de vendas da empresa."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Consultar receita por categoria (Priority: P1)

Como analista de vendas, quero somar receitas por categoria para comparar o desempenho das categorias.

**Why this priority**: Comparação por categoria oferece visão direta do desempenho por produto.

**Independent Test**: Fornecer registros com categorias repetidas e receitas conhecidas; verificar soma correta por categoria.

**Acceptance Scenarios**:

1. **Given** registros de venda com receita e categoria, **When** as métricas são calculadas, **Then** cada categoria contém a soma de suas receitas arredondada a duas casas decimais.
2. **Given** registros de categorias distintas, **When** as métricas são calculadas, **Then** cada categoria aparece uma vez com seu total correspondente.

---

### User Story 2 - Consultar receita por região (Priority: P2)

Como analista de vendas, quero somar receitas por região para comparar o desempenho regional.

**Why this priority**: Totais regionais apoiam comparação entre áreas de venda.

**Independent Test**: Fornecer registros com regiões repetidas e receitas conhecidas; verificar soma correta por região.

**Acceptance Scenarios**:

1. **Given** registros de venda com receita e região, **When** as métricas são calculadas, **Then** cada região contém a soma de suas receitas arredondada a duas casas decimais.

---

### User Story 3 - Consultar receita total da empresa (Priority: P3)

Como analista de vendas, quero conhecer a receita total da empresa no conjunto analisado.

**Why this priority**: Total geral fornece visão consolidada e valida os agregados segmentados.

**Independent Test**: Fornecer registros com receitas conhecidas; verificar soma total arredondada a duas casas decimais.

**Acceptance Scenarios**:

1. **Given** uma coleção de vendas com receita, **When** as métricas são calculadas, **Then** o total geral corresponde à soma das receitas, arredondada a duas casas decimais.

### Edge Cases

- Uma coleção vazia resulta em total geral igual a zero e agregados vazios.
- Uma única venda gera totais iguais à sua receita para categoria, região e total geral.
- Valores acumulados são arredondados a duas casas decimais nos agregados e no total geral.
- Cada registro de entrada possui `categoria`, `regiao` e `receita_total` válidos, produzidos pelas etapas anteriores.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema deve calcular a receita total de vendas agrupada por categoria.
- **FR-002**: O sistema deve calcular a receita total de vendas agrupada por região.
- **FR-003**: O sistema deve calcular a receita geral de todas as vendas.
- **FR-004**: Os totais por categoria, por região e o total geral devem ser apresentados arredondados a duas casas decimais.
- **FR-005**: O cálculo deve processar cada registro válido uma única vez e retornar os resultados separados por total geral, categoria e região.

### Key Entities

- **Registro de venda**: Venda individual com categoria, região e receita total já calculada.
- **Métricas agregadas**: Totais de receita consolidados por categoria, por região e para a empresa.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% dos registros válidos contribuem exatamente uma vez para seus totais por categoria, região e total geral.
- **SC-002**: Totais por categoria, região e total geral correspondem às somas esperadas com precisão de duas casas decimais.
- **SC-003**: Coleção vazia produz total geral zero e nenhum grupo, sem erro.
- **SC-004**: Totais por categoria e região podem ser comparados diretamente e reconciliam com total geral, salvo diferenças de arredondamento acumulado inferiores a um centavo por grupo.

## Assumptions

- A entrada contém registros limpos com `categoria`, `regiao` e `receita_total` numérica e finita.
- Os valores de `receita_total` já foram calculados e arredondados na etapa anterior.
- Categorias e regiões são agrupadas pelos valores recebidos, sem normalização adicional.
- O resultado contém total geral, totais por categoria e totais por região; apresentação ou exportação dessas métricas está fora do escopo desta funcionalidade.
