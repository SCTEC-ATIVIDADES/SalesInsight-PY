# Feature Specification: RF06 – Segmentar Clientes por Nível de Gasto

**Feature Branch**: `006-client-spending-segmentation`

**Created**: 2026-10-29

**Status**: Draft

**Input**: User description: "Calcular o total de compras por cliente e classificá-los em categorias: abaixo de R$ 3.000 = Bronze; R$ 3.000 a R$ 8.000 = Prata; acima de R$ 8.000 = Ouro."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Identificar segmento de gasto por cliente (Priority: P1)

Como analista de vendas, quero ver o gasto total e segmento de cada cliente para reconhecer níveis de valor e priorizar ações comerciais.

**Why this priority**: Segmentação completa entrega o valor principal da funcionalidade.

**Independent Test**: Fornecer vendas de vários clientes, inclusive clientes repetidos, e conferir os totais e segmentos resultantes de forma independente.

**Acceptance Scenarios**:

1. **Given** vendas associadas a clientes com gastos totais abaixo de R$ 3.000, de R$ 3.000 a R$ 8.000 e acima de R$ 8.000, **When** a segmentação é consultada, **Then** esses clientes são classificados respectivamente como Bronze, Prata e Ouro.
2. **Given** várias vendas para o mesmo cliente, **When** a segmentação é calculada, **Then** todas as receitas desse cliente são somadas antes da classificação e o resultado apresenta total gasto arredondado a duas casas decimais.
3. **Given** um cliente com gasto exatamente R$ 3.000 ou R$ 8.000, **When** seu segmento é calculado, **Then** ele é classificado como Prata.
4. **Given** vendas de clientes distintos, **When** a segmentação é calculada, **Then** cada cliente aparece uma única vez e totais não são misturados entre clientes.

### Edge Cases

- Uma coleção vazia retorna nenhum cliente segmentado.
- Cliente com uma única compra é classificado pelo valor dessa compra.
- Gasto total negativo, se presente em entradas válidas, segue os mesmos limites e fica Bronze quando abaixo de R$ 3.000.
- Entradas são vendas válidas com identificação do cliente e receita total numérica; validação/limpeza dessas entradas pertence a etapa anterior do pipeline.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Sistema MUST somar a receita total de todas as compras de cada cliente individualmente.
- **FR-002**: Sistema MUST classificar gasto total inferior a R$ 3.000 como Bronze.
- **FR-003**: Sistema MUST classificar gasto total de R$ 3.000 até R$ 8.000, inclusive, como Prata.
- **FR-004**: Sistema MUST classificar gasto total superior a R$ 8.000 como Ouro.
- **FR-005**: Sistema MUST apresentar, para cada cliente, total gasto arredondado a duas casas decimais e seu segmento.
- **FR-006**: Sistema MUST produzir resultado vazio quando não houver vendas.

### Key Entities *(include if feature involves data)*

- **Cliente**: Identidade que agrupa compras; possui gasto total acumulado e segmento atribuído.
- **Compra**: Registro associado a um cliente e contendo receita total usada no cálculo do gasto.
- **Segmento de gasto**: Categoria Bronze, Prata ou Ouro definida pelos limites de gasto total.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% dos clientes em uma amostra de referência recebem total gasto igual à soma das próprias compras, arredondada a duas casas.
- **SC-002**: 100% dos clientes são atribuídos ao segmento correto, inclusive para gastos exatamente nos limites R$ 3.000 e R$ 8.000.
- **SC-003**: Nenhum cliente ou compra de outro cliente altera o total e segmento calculados para um cliente específico.
- **SC-004**: Para entrada vazia, sistema retorna zero clientes segmentados.

## Assumptions

- A identidade do cliente e a receita de cada compra já estão presentes e válidas nos registros recebidos.
- A classificação usa gasto total acumulado antes de arredondar o valor exibido; as entradas financeiras válidas têm precisão adequada para a regra de negócio.
- Os intervalos são inclusivos em R$ 3.000 e R$ 8.000 para Prata, conforme tabela e exemplo fornecidos.
- A segmentação deve ser incluída no fluxo atual de métricas e exportada pelos relatórios existentes; criação de novos formatos de relatório fica fora do escopo.