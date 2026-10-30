# Feature Specification: RF02 – Inspecionar e Descrever os Dados

**Feature Branch**: `002-data-inspection`

**Created**: 2026-10-28

**Status**: Draft

**Input**: User description: "RF02 – Inspecionar e Descrever os Dados: Criar uma função no módulo para exibir a quantidade total de registros carregados e verificar linhas com dados incompletos ou nulos. Exemplo de função: `def inspecionar_dados(dados): print(\"\\n=== INSPEÇÃO INICIAL DOS DADOS ===\") print(f\"Total de registros carregados: {len(dados)}\") if dados: print(f\"Campos disponíveis: {list(dados[0].keys())}\") print(f\"Exemplo do primeiro registro: {dados[0]}\")`"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Exibição do Panorama Geral e Estrutura Inicial dos Dados Carregados (Priority: P1)

Como analista de dados ou avaliador executando o pipeline de vendas, preciso visualizar imediatamente o total de registros carregados, a lista de campos (colunas) disponíveis e uma amostra do primeiro registro logo após a leitura do dataset bruto, para confirmar que a fonte de dados foi lida com a estrutura esperada antes de iniciar a higienização.

**Why this priority**: Esta é a saída principal exigida no exemplo de referência do RF02 e garante visibilidade imediata sobre o volume bruto e o esquema de colunas carregado em memória.

**Independent Test**: Pode ser testado de forma independente fornecendo uma coleção conhecida de registros de vendas à rotina de inspeção e verificando se a saída apresenta o cabeçalho de inspeção, a contagem exata de registros, os nomes dos campos do cabeçalho e o primeiro registro como amostra.

**Acceptance Scenarios**:

1. **Given** uma coleção não vazia de registros de vendas carregados em memória, **When** a rotina de inspeção inicial dos dados é executada, **Then** o sistema exibe o título da seção (`=== INSPEÇÃO INICIAL DOS DADOS ===`), o total exato de registros carregados, a lista de campos disponíveis extraída das chaves dos registros e o exemplo completo do primeiro registro.
2. **Given** o dataset padrão do projeto carregado com 8 colunas (`id_venda`, `data_venda`, `cliente`, `produto`, `categoria`, `regiao`, `quantidade`, `preco_unitario`), **When** a rotina de inspeção é acionada no fluxo principal, **Then** todos os 8 campos disponíveis são listados na ordem original do cabeçalho sem omitir ou alterar os valores brutos do registro de amostra.

---

### User Story 2 - Verificação e Contabilização de Linhas com Dados Incompletos ou Nulos (Priority: P2)

Como analista de dados auditando a qualidade da base bruta, preciso que a inspeção identifique e contabilize quantas linhas possuem valores incompletos, vazios ou nulos (e em quais campos ocorrem), para dimensionar o nível de ruído do dataset antes da etapa de limpeza e descarte.

**Why this priority**: Complementa a descrição estrutural cumprindo a segunda parte explícita do requisito RF02 ("verificar linhas com dados incompletos ou nulos"), fornecendo diagnóstico essencial para auditoria dos dados brutos gerados no RF01.

**Independent Test**: Pode ser testado fornecendo uma coleção de registros contendo linhas completas e linhas com campos vazios, apenas espaços em branco ou nulos (ex.: `quantidade=""` ou `preco_unitario=None`) e verificando se a rotina reporta e retorna a contagem exata de registros incompletos sem modificar os dados originais.

**Acceptance Scenarios**:

1. **Given** uma coleção de registros contendo linhas com valores vazios (`""`), compostos apenas por espaços em branco ou nulos (`None`) em qualquer campo, **When** a rotina de inspeção é executada, **Then** o sistema identifica e informa o total de linhas com dados incompletos ou nulos, além do detalhamento de ocorrências ausentes por campo.
2. **Given** uma coleção de registros onde todos os campos de todas as linhas estão devidamente preenchidos, **When** a rotina de inspeção é executada, **Then** o sistema informa que existem 0 registros incompletos ou nulos.
3. **Given** uma coleção de registros brutos passada para a inspeção, **When** a verificação de nulos e incompletos é concluída, **Then** a coleção original permanece 100% inalterada (sem mutação ou remoção prematura de linhas).

---

### User Story 3 - Comportamento Seguro para Coleção de Dados Vazia (Priority: P3)

Como usuário executando o pipeline em cenários onde o arquivo de entrada está vazio ou não pôde ser carregado, preciso que a inspeção trate coleções vazias de forma segura, exibindo total zero sem falhar ao tentar acessar o primeiro registro.

**Why this priority**: Previne erros de índice (`IndexError`) quando `carregar_csv` retorna uma lista vazia devido a arquivo ausente ou sem linhas de dados, mantendo a resiliência operacional exigida no projeto.

**Independent Test**: Pode ser testado invocando a rotina de inspeção com uma lista vazia (`[]`) e verificando que o sistema exibe `Total de registros carregados: 0` sem lançar exceções e sem tentar imprimir campos ou primeiro registro inexistentes.

**Acceptance Scenarios**:

1. **Given** uma coleção de dados vazia (`[]`), **When** a rotina de inspeção é chamada, **Then** o sistema exibe o cabeçalho de inspeção e `Total de registros carregados: 0` sem tentar acessar o primeiro elemento e sem interromper a execução com erro.

### Edge Cases

- O que acontece quando a coleção de dados está vazia (`[]`)? O sistema exibe `Total de registros carregados: 0`, omite a exibição de campos disponíveis e do primeiro registro (conforme a guarda `if dados:`), e reporta zero registros incompletos sem levantar erro de índice.
- Como o sistema classifica um campo preenchido apenas com espaços em branco (ex.: `"   "`) ou string vazia (`""`) vindo da leitura CSV? Ambos são contabilizados como valores incompletos/nulos durante a verificação, assim como valores `None`.
- O que acontece quando um mesmo registro possui múltiplos campos vazios ou nulos simultaneamente (ex.: `quantidade` e `preco_unitario` vazios na mesma linha)? A contagem de linhas incompletas contabiliza a linha uma única vez no total de registros com problemas, enquanto a contagem por coluna reflete a ausência em cada campo afetado.
- A inspeção altera ou remove registros com espaços sobressalentes ou valores nulos? Não; a inspeção é estritamente diagnóstica e somente-leitura, preservando os dados brutos intactos para a etapa subsequente de limpeza.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O módulo de vendas DEVE disponibilizar uma função reutilizável (`inspecionar_dados(dados)`) que receba a coleção de registros carregados e realize o diagnóstico inicial do dataset sem modificar os dados de entrada.
- **FR-002**: A função de inspeção DEVE exibir no console o cabeçalho `=== INSPEÇÃO INICIAL DOS DADOS ===` e a linha `Total de registros carregados: <N>`, onde `<N>` corresponde à quantidade total de registros presentes na coleção recebida.
- **FR-003**: Quando a coleção de dados não estiver vazia, a função DEVE exibir a lista de campos disponíveis (`Campos disponíveis: [...]`) obtida a partir das chaves do primeiro registro e exibir a amostra do primeiro registro (`Exemplo do primeiro registro: {...}`).
- **FR-004**: A função de inspeção DEVE verificar todos os registros carregados para identificar linhas com dados incompletos ou nulos, considerando como ausente/nulo qualquer valor `None`, string vazia (`""`) ou string composta exclusivamente por espaços em branco.
- **FR-005**: A função de inspeção DEVE exibir no resumo de inspeção a quantidade total de registros (linhas) que possuem ao menos um campo incompleto ou nulo, permitindo visualizar imediatamente a presença de inconsistências no dataset bruto.
- **FR-006**: A função de inspeção DEVE retornar um resumo estruturado (dicionário) contendo ao menos o total de registros carregados (`total_registros`), a lista de campos disponíveis (`campos`), o total de linhas com dados incompletos ou nulos (`registros_incompletos`) e a contagem de valores nulos/vazios por campo (`nulos_por_campo`), facilitando asserções diretas em testes automatizados além da saída em console.
- **FR-007**: Quando a coleção recebida estiver vazia (`[]`), a função DEVE executar sem erros, exibindo `Total de registros carregados: 0` e retornando a estrutura de resumo zerada (`total_registros=0`, `campos=[]`, `registros_incompletos=0`, `nulos_por_campo={}`).
- **FR-008**: O ponto de entrada principal do sistema (`main.py`) DEVE integrar a chamada de inspeção logo após o carregamento do dataset de vendas, exibindo o diagnóstico inicial durante a execução padrão do pipeline.

### Key Entities *(include if feature involves data)*

- **Registro de Venda Bruto**: Dicionário representando uma linha carregada do dataset de vendas contendo os campos `id_venda`, `data_venda`, `cliente`, `produto`, `categoria`, `regiao`, `quantidade` e `preco_unitario`, cujos valores brutos podem estar preenchidos, vazios (`""`) ou nulos (`None`).
- **Resumo de Inspeção de Dados**: Estrutura diagnóstica resultante da inspeção inicial, composta pelo volume total de registros (`total_registros`), lista de colunas detectadas (`campos`), primeiro registro de amostra (`primeiro_registro`), total de linhas com ao menos um campo incompleto/nulo (`registros_incompletos`) e mapa de contagem de valores ausentes por coluna (`nulos_por_campo`).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% das execuções da rotina de inspeção sobre um dataset carregado exibem exatamente a quantidade total de registros, a lista completa de campos disponíveis, o exemplo do primeiro registro e o total de linhas incompletas/nulas em menos de 1 segundo para volumes de até 10.000 registros.
- **SC-002**: 100% das linhas contendo qualquer campo vazio (`""`), preenchido apenas com espaços (`"   "`) ou nulo (`None`) são detectadas e contabilizadas com precisão no indicador de registros incompletos e no detalhamento por campo.
- **SC-003**: 0 mutações ou efeitos colaterais ocorrem sobre a coleção de registros fornecida como entrada durante ou após a execução da inspeção.
- **SC-004**: 100% das chamadas com coleções vazias (`[]`) executam sem falhas ou exceções não tratadas, reportando 0 registros carregados e 0 registros incompletos.

## Assumptions

- Os dados fornecidos para `inspecionar_dados(dados)` seguem o formato retornado por `carregar_csv`: uma lista de dicionários (`list[dict[str, str | None]]`) onde cada dicionário representa uma linha do dataset mapeada pelas colunas do cabeçalho.
- A saída de console mantém exatamente as mensagens demonstradas no exemplo do requisito (`=== INSPEÇÃO INICIAL DOS DADOS ===`, `Total de registros carregados: ...`, `Campos disponíveis: ...`, `Exemplo do primeiro registro: ...`) e adiciona a linha informativa sobre a verificação de linhas com dados incompletos ou nulos logo a seguir, garantindo compatibilidade total com o exemplo fornecido e com o requisito completo do RF02.
- Embora `inspecionar_dados(dados)` imprima o relatório diagnóstico na saída padrão (conforme o exemplo do RF02), retornar também um dicionário com as métricas apuradas não interfere no uso como procedimento (`print`) e torna a verificação de testes unitários mais simples, explícita e determinística.
