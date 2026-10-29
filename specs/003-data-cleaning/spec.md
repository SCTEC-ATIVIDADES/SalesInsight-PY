# Feature Specification: RF03 – Limpar e Tratar os Dados

**Feature Branch**: `003-data-cleaning`

**Created**: 2026-10-29

**Status**: Draft

**Input**: User description: "RF03 – Limpar e Tratar os Dados. A função deve ler a lista de dicionários, remover espaços extras nas strings (`.strip()`), ignorar/filtrar registros com valores vazios ou inválidos para `quantidade` e `preco_unitario`, e converter esses campos para `int` e `float`. Registros válidos devem ser devolvidos em lista limpa, reportando quantos foram válidos e removidos."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Normalizar registros válidos (Priority: P1)

Como analista de vendas, quero receber registros consistentes, com espaços externos removidos e tipos numéricos apropriados, para que as etapas seguintes possam analisar os dados de forma confiável.

**Why this priority**: Produzir registros limpos e utilizáveis é o propósito central desta etapa do pipeline.

**Independent Test**: Fornecer registros válidos com espaços em campos textuais e valores numéricos como texto; verificar os textos normalizados, a quantidade inteira, o preço decimal e a preservação dos demais campos de venda.

**Acceptance Scenarios**:

1. **Given** um registro com campos textuais cercados por espaços e valores numéricos válidos, **When** a limpeza é executada, **Then** o registro resultante tem os espaços externos removidos e quantidade e preço convertidos para seus tipos numéricos correspondentes.
2. **Given** uma lista com vários registros válidos, **When** a limpeza é executada, **Then** todos são devolvidos na mesma ordem em uma coleção de dados limpos.

---

### User Story 2 - Excluir dados inválidos e reportar o resultado (Priority: P2)

Como analista, quero que registros com quantidade ou preço ausente ou inválido sejam descartados e contabilizados, para evitar que dados impróprios contaminem as análises.

**Why this priority**: A validação impede que valores ausentes ou não numéricos sejam tratados como vendas válidas e torna a qualidade do resultado visível.

**Independent Test**: Fornecer registros com campos numéricos vazios, compostos por espaços ou não conversíveis; verificar que são excluídos e que as contagens de válidos e removidos correspondem à entrada.

**Acceptance Scenarios**:

1. **Given** um registro com quantidade ou preço vazio ou composto apenas por espaços, **When** a limpeza é executada, **Then** o registro é ignorado e contado como removido.
2. **Given** um registro com quantidade não inteira ou preço não numérico, **When** a limpeza é executada, **Then** o registro é ignorado e contado como removido sem interromper o processamento dos demais.
3. **Given** uma coleção contendo registros válidos e inválidos, **When** a limpeza é concluída, **Then** o relatório apresenta as contagens exatas de válidos e removidos.

### Edge Cases

- Uma lista vazia resulta em lista limpa vazia e contagens de válidos e removidos iguais a zero.
- Quantidade ou preço contendo somente espaços é considerado vazio após normalização.
- Valores numéricos que não possam ser convertidos ao tipo requerido tornam o registro inválido; os demais registros continuam a ser processados.
- A função trabalha sobre os registros de entrada sem alterar os valores da lista original.
- A ausência de qualquer campo do esquema esperado (`id_venda`, `data_venda`, `cliente`, `produto`, `categoria`, `regiao`, `quantidade`, `preco_unitario`) torna a linha malformada e removida, contabilizada uma única vez pelo primeiro motivo detectado na ordem de validação do esquema: campos ausentes, campos textuais (data, cliente, produto, categoria, região), quantidade, preço unitário e identificador.
- Valores nulos ou vazios após remoção dos espaços em campos textuais obrigatórios tornam a linha malformada e removida; datas devem representar datas válidas no formato estabelecido pelo dataset (`YYYY-MM-DD`).
- Identificador ausente ou não conversível para inteiro torna a linha malformada e removida.
- Preços não finitos (`NaN`, infinito positivo ou negativo) são inválidos e removidos.
- Duplicatas exatas são identificadas após normalizar e converter os campos; somente a primeira ocorrência permanece, e cada repetição é removida uma vez com motivo `registro_duplicado`. Linhas distintas que compartilham o identificador são preservadas.
- A linha removida deve ser contabilizada por um único motivo primário determinístico, usando a ordem de validação descrita acima; totais por motivo devem somar o total de removidos.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema DEVE aceitar uma coleção de registros de venda estruturados como dicionários e produzir uma coleção separada de registros limpos.
- **FR-002**: O sistema DEVE remover espaços externos dos campos textuais do registro, incluindo cliente, produto, categoria, região e data da venda.
- **FR-003**: O sistema DEVE remover qualquer registro cuja quantidade ou preço unitário esteja ausente, vazio ou composto somente por espaços; ausências devem ser contabilizadas em motivo específico distinto de valores presentes, porém inválidos.
- **FR-004**: O sistema DEVE converter a quantidade de cada registro elegível para número inteiro e o preço unitário para número decimal.
- **FR-005**: O sistema DEVE remover registros cujos valores de quantidade ou preço unitário não possam ser convertidos aos tipos requeridos, incluindo preço não finito, com motivo específico distinto para quantidade inválida e preço inválido, sem interromper o processamento da coleção.
- **FR-006**: Para registros aceitos, o sistema DEVE preservar os campos da venda e normalizar o identificador para inteiro; campos ausentes, identificador não conversível, campos textuais obrigatórios nulos ou vazios após normalização, ou data vazia/inválida após normalização tornam a linha malformada e removida.
- **FR-007**: O sistema DEVE informar no relatório a quantidade de registros válidos e removidos, com contagens estruturadas por um único motivo primário por linha rejeitada, disponibilizar os contadores para exportação e devolver os registros válidos na ordem de entrada, removendo ocorrências duplicadas exatas após normalização e preservando a primeira.
- **FR-008**: O sistema DEVE deixar a coleção original inalterada durante a limpeza. Duas linhas são duplicatas quando todos os oito campos normalizados são iguais; igualdade isolada de `id_venda` não caracteriza duplicidade.
- **FR-009**: Uma coleção vazia DEVE ser processada sem erro e produzir zero registros válidos, zero removidos e contadores de motivos iguais a zero.

### Key Entities *(include if data involved)*

- **Registro bruto de venda**: Dicionário de uma venda recebida da etapa de carregamento, contendo identificador, data, cliente, produto, categoria, região, quantidade e preço unitário, possivelmente ainda como texto.
- **Registro limpo de venda**: Registro aceito com textos sem espaços externos, identificador e quantidade inteiros e preço unitário decimal.
- **Relatório de limpeza**: Resumo com o total de registros válidos e removidos durante o processamento.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% dos registros com quantidade e preço válidos são preservados na saída, com valores numéricos nos tipos requeridos e espaços externos removidos dos campos textuais.
- **SC-002**: 100% dos registros com quantidade ou preço ausente, vazio ou não conversível são excluídos e incluídos na contagem de removidos.
- **SC-003**: Em todas as execuções, a soma de registros válidos e removidos é igual ao total de registros de entrada.
- **SC-004**: A coleção original permanece inalterada após o processamento, inclusive quando registros inválidos são encontrados.
- **SC-005**: Uma coleção vazia resulta em zero registros válidos e zero removidos, todos os contadores por motivo em zero, sem falhas.
- **SC-006**: Para qualquer entrada, a soma dos contadores estruturados por motivo é exatamente igual à quantidade de registros removidos.
- **SC-007**: Para cada grupo de linhas equivalentes nos oito campos normalizados, exatamente uma ocorrência é preservada, mantendo a ordem da primeira ocorrência.

## Assumptions

- A entrada segue o formato de lista de dicionários de vendas estabelecido pelas etapas anteriores do pipeline.
- O esquema possui os oito campos especificados; qualquer campo ausente, valor nulo em campo textual obrigatório, identificador não conversível ou data vazia após normalização torna a linha malformada e removida.
- Datas devem ser datas válidas no formato `YYYY-MM-DD`; preços devem ser finitos.
- A conversão decimal segue as regras numéricas aceitas pelo formato dos dados de entrada; normalização de separadores decimais não está incluída.
- O relatório é apresentado ao usuário ao término da limpeza, e a função retorna somente a coleção de registros limpos.