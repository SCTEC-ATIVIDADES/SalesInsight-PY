# Feature Specification: RF04 – Criar Campos Derivados

**Feature Branch**: `004-derived-fields`

**Created**: 2026-10-29

**Status**: Draft

**Input**: User description: "RF04 – Criar Campos Derivados. Adicionar a cada registro `receita_total`, calculada como `quantidade * preco_unitario` arredondada a duas casas decimais, e `faixa_preco`: Baixo (< R$ 500), Médio (de R$ 500 até R$ 2.000 inclusive) e Alto (> R$ 2.000)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Calcular receita por registro (Priority: P1)

Como analista de vendas, quero que cada registro tenha sua receita total para poder analisar o valor gerado por venda.

**Why this priority**: Receita total é o valor derivado central e base para categorizar registros.

**Independent Test**: Fornecer registros com quantidade e preço unitário conhecidos; verificar receita por registro arredondada a duas casas decimais.

**Acceptance Scenarios**:

1. **Given** um registro com quantidade e preço unitário válidos, **When** os campos derivados são criados, **Then** o registro inclui receita total igual ao produto, arredondado a duas casas decimais.
2. **Given** vários registros, **When** os campos derivados são criados, **Then** cada registro recebe seu próprio valor calculado e os demais dados permanecem disponíveis.

---

### User Story 2 - Classificar registros por faixa de receita (Priority: P2)

Como analista de vendas, quero classificar cada venda por faixa de receita para comparar vendas de baixo, médio e alto valor.

**Why this priority**: A faixa torna o valor calculado diretamente utilizável em análises segmentadas.

**Independent Test**: Fornecer registros cuja receita fique abaixo, nos limites e acima dos limiares; verificar cada faixa atribuída.

**Acceptance Scenarios**:

1. **Given** receita menor que R$ 500, **When** o registro é classificado, **Then** a faixa é "Baixo".
2. **Given** receita igual a R$ 500 ou até R$ 2.000 inclusive, **When** o registro é classificado, **Then** a faixa é "Médio".
3. **Given** receita maior que R$ 2.000, **When** o registro é classificado, **Then** a faixa é "Alto".

### Edge Cases

- Receita exatamente R$ 500 deve pertencer à faixa "Médio"; exatamente R$ 2.000 também deve pertencer à faixa "Médio".
- Receita calculada deve ser arredondada para duas casas antes da classificação.
- Considera-se que os registros recebidos possuem quantidade e preço unitário válidos, conforme etapa anterior de limpeza.
- Lista vazia deve resultar em lista vazia, sem falha.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Cada registro de venda deve receber campo `receita_total`, calculado pela quantidade multiplicada pelo preço unitário e arredondado para duas casas decimais.
- **FR-002**: Cada registro deve receber campo `faixa_preco` com valor "Baixo" quando receita total for inferior a R$ 500.
- **FR-003**: Cada registro deve receber campo `faixa_preco` com valor "Médio" quando receita total estiver entre R$ 500 e R$ 2.000, inclusive.
- **FR-004**: Cada registro deve receber campo `faixa_preco` com valor "Alto" quando receita total for superior a R$ 2.000.
- **FR-005**: A transformação deve preservar os registros e seus demais campos, mantendo a ordem recebida.

### Key Entities *(include if feature involves data)*

- **Registro de venda**: Venda individual com quantidade e preço unitário; passa a incluir receita total e faixa de receita calculadas.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% dos registros válidos processados contêm `receita_total` correta, arredondada a duas casas.
- **SC-002**: 100% dos registros válidos são classificados corretamente, incluindo valores exatamente nos limites de R$ 500 e R$ 2.000.
- **SC-003**: Todos os campos originais e a ordem dos registros permanecem preservados após a transformação.
- **SC-004**: A transformação processa cada registro uma única vez e suporta o volume corrente de até 10.000 registros sem perda de dados.

## Assumptions

- Os campos `quantidade` e `preco_unitario` já foram validados e convertidos pela etapa de limpeza anterior.
- A classificação usa o valor de `receita_total` após arredondamento a duas casas decimais.
- A transformação opera sobre uma lista de registros e retorna essa lista com os campos derivados adicionados.
