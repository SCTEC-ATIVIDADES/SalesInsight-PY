# Feature Specification: RF01 – Criar ou Carregar o Dataset de Vendas

**Feature Branch**: `001-sales-dataset-generator`

**Created**: 2026-10-26

**Status**: Draft

**Input**: User description: "RF01 – Criar ou Carregar o Dataset de Vendas: O projeto deverá ter um dataset de vendas. O estudante pode gerar o dataset sinteticamente no próprio código (recomendado para facilitar a reprodução) ou utilizar um arquivo CSV real. Opção B – Usar IA para gerar o CSV: O estudante pode usar uma IA e solicitar que gere o arquivo CSV, desde que contenha ao menos as colunas: data, produto, categoria, quantidade, preço e região. O mínimo de registros é 100. Para gerar os dados do csv, vamos usar uma lib para gerar dados reais/mockados/fakes. A geração dos dados fica em um arquivo/módulo independente."

## Clarifications

### Session 2026-10-28

- Q: Como o ambiente virtual Python (`venv`) deve se relacionar com o ambiente padronizado do projeto? → A: Option A - Manter Docker e adicionar suporte oficial a `.venv` (`python -m venv .venv`) para execução local isolada.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Geração Automatizada do Dataset de Vendas com Dados Realistas e Ruídos Controlados (Priority: P1)

Como analista de dados ou avaliador executando o projeto pela primeira vez em qualquer ambiente, preciso que o sistema gere automaticamente um conjunto de dados de vendas realista (com no mínimo 100 registros) contendo tanto registros válidos quanto inconsistências deliberadas (valores ausentes, espaços sobressalentes e duplicatas), para que o pipeline de análise e limpeza possa ser reproduzido e validado imediatamente sem depender de arquivos externos pré-existentes.

**Why this priority**: Sem a criação determinística do conjunto de dados de vendas contendo os campos obrigatórios e os cenários de inconsistência, nenhuma das etapas subsequentes do pipeline (inspeção, limpeza, transformação, agregação e exportação) pode ser executada ou validada.

**Independent Test**: Pode ser testado de forma independente acionando a rotina de geração do dataset apontando para um caminho de destino temporário com uma semente fixa e verificando se o arquivo é criado com o cabeçalho exato, volume mínimo de 100 registros, dados realistas e presença controlada de ruídos (nulos, espaços extras e duplicidade).

**Acceptance Scenarios**:

1. **Given** que o arquivo de dados de vendas ainda não existe no caminho informado, **When** a rotina de geração do dataset é executada com os parâmetros padrão, **Then** um arquivo estruturado é criado contendo cabeçalho completo (`id_venda`, `data_venda`, `cliente`, `produto`, `categoria`, `regiao`, `quantidade`, `preco_unitario`) e pelo menos 100 registros gerados.
2. **Given** uma semente de geração definida (ex.: `seed=42`) e uma quantidade solicitada de registros (ex.: `100`), **When** a geração do dataset é executada duas vezes consecutivas, **Then** ambos os arquivos produzidos possuem exatamente o mesmo conteúdo, garantindo reprodutibilidade total.
3. **Given** a geração de um novo dataset sintético/mockado, **When** os registros gerados são inspecionados, **Then** verifica-se a presença deliberada de registros com espaços extras em textos (aprox. 10%), valores vazios em quantidade ou preço unitário (aprox. 5% cada) e pelo menos um registro duplicado para exercitar as regras futuras de limpeza.

---

### User Story 2 - Carregamento Estruturado do Dataset de Vendas Existente (Priority: P2)

Como analista de dados, preciso carregar um arquivo de vendas existente no sistema para uma estrutura em memória organizada por registros e colunas nomeadas, para que os dados brutos possam ser inspecionados e processados pelas demais funções do pipeline sem perda de informação e sem depender de caminhos absolutos fixos.

**Why this priority**: Permite tanto a leitura imediata do dataset recém-gerado quanto a utilização de qualquer arquivo de vendas compatível fornecido pelo usuário, cumprindo a exigência de leitura parametrizada da fonte de dados.

**Independent Test**: Pode ser testado fornecendo um arquivo de vendas conhecido com registros válidos e incompletos e verificando se a rotina retorna a coleção exata de registros mapeados pelos nomes das colunas do cabeçalho.

**Acceptance Scenarios**:

1. **Given** um arquivo de vendas válido existente no caminho relativo ou parametrizado informado, **When** a rotina de carregamento é executada, **Then** todos os registros do arquivo são disponibilizados em memória preservando os nomes das colunas do cabeçalho e os valores brutos originais (incluindo vazios e espaços).
2. **Given** que o pipeline principal é iniciado em um diretório onde o arquivo padrão `vendas.csv` já existe, **When** o fluxo de entrada verifica a fonte de dados, **Then** o sistema carrega o arquivo existente diretamente sem sobrescrevê-lo desnecessariamente.

---

### User Story 3 - Tratamento Resiliente de Caminhos e Falhas de Acesso à Fonte de Dados (Priority: P3)

Como usuário executando o pipeline, preciso receber mensagens claras e um comportamento seguro caso o caminho do arquivo de vendas informado seja inexistente, esteja vazio ou não possa ser lido, para diagnosticar rapidamente problemas de entrada sem que o sistema encerre abruptamente com falhas não tratadas.

**Why this priority**: Garante robustez operacional e atende aos critérios de avaliação de qualidade e resiliência contra falhas de entrada/saída e caminhos inválidos.

**Independent Test**: Pode ser testado invocando a rotina de carregamento com um caminho de arquivo inexistente ou um arquivo sem registros e verificando se o sistema reporta a situação de forma clara e retorna uma estrutura vazia segura ou erro controlado.

**Acceptance Scenarios**:

1. **Given** um caminho para um arquivo de vendas que não existe no sistema de arquivos, **When** a função de carregamento direto é chamada, **Then** o sistema informa claramente que o arquivo não foi encontrado sem interromper a execução com rastros de erro brutos não tratados.
2. **Given** um caminho de destino em um subdiretório ainda não existente para a geração do dataset, **When** a função de criação do dataset é chamada, **Then** o diretório necessário é preparado ou o arquivo é gravado corretamente no caminho relativo especificado.

### Edge Cases

- O que acontece quando o número de registros solicitado na geração é menor que o mínimo exigido pelo projeto (100 registros)? O sistema deve aceitar o parâmetro explícito para fins de testes unitários rápidos, mas utilizar no mínimo 100 registros como padrão operacional.
- Como o sistema lida com um arquivo CSV existente que contém apenas a linha de cabeçalho e nenhum registro de venda? A rotina de carregamento deve retornar uma coleção vazia sem falhar.
- O que acontece quando o arquivo possui caracteres acentuados (ex.: `Eletrônicos`, `Acessórios`, `Médio`)? A leitura e a escrita devem preservar integralmente a codificação de caracteres padrão em qualquer sistema operacional.
- Como o sistema se comporta se a linha duplicada inserida no arquivo gerado for lida? O carregamento bruto deve manter todas as linhas presentes no arquivo (por exemplo, `n_registros` mais a linha duplicada, ou totalizando o volume gerado) para que a etapa posterior de limpeza e deduplicação possa identificá-la e contabilizá-la.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema DEVE disponibilizar uma rotina reutilizável em um arquivo/módulo independente dedicado exclusivamente à geração de dados para criar um dataset de vendas contendo dados mockados/fakes realistas quando o arquivo de entrada não existir ou quando solicitado explicitamente, mantendo a responsabilidade de geração desacoplada do módulo de processamento e leitura do pipeline.
- **FR-002**: O dataset gerado DEVE conter obrigatoriamente as colunas `id_venda`, `data_venda`, `cliente`, `produto`, `categoria`, `regiao`, `quantidade` e `preco_unitario`, contemplando todos os campos exigidos para análise (data, produto, categoria, quantidade, preço e região, além de identificador e cliente).
- **FR-003**: A geração do dataset DEVE produzir no mínimo 100 registros por padrão (ex.: `n_registros=100` na função e `150` na execução de demonstração em `main.py`, permitindo parametrização da quantidade de registros e do caminho do arquivo de destino, tendo `vendas.csv` como caminho relativo padrão).
- **FR-004**: A geração de dados DEVE aceitar uma semente de aleatoriedade (`seed`, padrão `42`) que garanta que a criação de dados mockados/fakes e a injeção de inconsistências sejam 100% determinísticas e reproduzíveis entre diferentes execuções.
- **FR-005**: O dataset gerado DEVE utilizar o catálogo de produtos (`Notebook`, `Smartphone`, `Tablet`, `Monitor`, `Teclado`, `Mouse`), suas respectivas categorias (`Eletrônicos`, `Celulares`, `Acessórios`) e as cinco regiões brasileiras (`Sudeste`, `Sul`, `Nordeste`, `Centro-Oeste`, `Norte`), combinados com dados mockados/fakes realistas para clientes, datas de venda (no formato `AAAA-MM-DD`) e preços unitários (entre 100,00 e 3500,00).
- **FR-006**: A rotina de geração DEVE injetar inconsistências controladas no arquivo gerado para viabilizar a validação das etapas posteriores de limpeza, incluindo: valores ausentes/vazios em `quantidade` (aprox. 5% de chance), valores ausentes/vazios em `preco_unitario` (aprox. 5% de chance), espaços em branco sobressalentes no início e fim do nome do `produto` (aprox. 10% de chance) e registro duplicado.
- **FR-007**: O sistema DEVE disponibilizar uma rotina parametrizada para carregar os registros de qualquer arquivo CSV de vendas compatível a partir de um caminho relativo ou informado, retornando uma coleção estruturada de registros indexados pelos nomes das colunas do cabeçalho.
- **FR-008**: Nenhuma rotina de geração ou carregamento DEVE depender de caminhos absolutos fixos (hardcoded), devendo operar corretamente a partir da raiz do projeto ou de caminhos fornecidos por parâmetro.
- **FR-009**: A rotina de carregamento DEVE tratar de forma segura e resiliente cenários de arquivo inexistente ou inacessível, emitindo mensagem clara de diagnóstico sem causar falha abrupta não tratada.
- **FR-010**: O projeto DEVE suportar e documentar a execução local isolada via ambiente virtual Python nativo (`python3 -m venv .venv` com instalação de `requirements.txt`), operando em complementaridade ao ambiente containerizado Docker Compose e garantindo que `.venv/` seja ignorado no versionamento e no contexto de build do container.

### Key Entities *(include if feature involves data)*

- **Registro de Venda Bruto**: Representa uma transação comercial lida ou gerada no arquivo CSV antes da higienização. Atributos: `id_venda` (identificador da transação), `data_venda` (data da ocorrência), `cliente` (identificador ou nome do comprador), `produto` (item comercializado, podendo conter espaços extras na entrada bruta), `categoria` (classificação do produto), `regiao` (região geográfica da venda), `quantidade` (volume de itens, podendo estar vazio na entrada bruta) e `preco_unitario` (valor unitário do item, podendo estar vazio na entrada bruta).
- **Catálogo de Referência de Vendas**: Conjunto de domínios válidos utilizados na geração de dados para manter coerência de negócio entre `produto` e `categoria`, limites de `preco_unitario` (100 a 3500), `quantidade` (1 a 8) e `regiao` (`Sudeste`, `Sul`, `Nordeste`, `Centro-Oeste`, `Norte`).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A execução da rotina de geração com os parâmetros padrão cria um arquivo `vendas.csv` válido contendo no mínimo 100 registros de vendas e todas as 8 colunas obrigatórias em menos de 2 segundos.
- **SC-002**: 100% das execuções de geração realizadas com a mesma semente (`seed`) e mesmo número de registros produzem arquivos de vendas idênticos byte a byte.
- **SC-003**: O dataset gerado com a semente padrão contém 100% dos tipos de inconsistências exigidos para teste do pipeline (pelo menos 1 registro com `quantidade` vazia, 1 registro com `preco_unitario` vazio, 1 registro com espaços sobressalentes em `produto` e 1 registro duplicado).
- **SC-004**: 100% dos registros presentes no arquivo `vendas.csv` são carregados em memória preservando a correspondência exata entre cabeçalho e valores, sem perda ou truncamento de caracteres acentuados.
- **SC-005**: 0 ocorrências de caminhos absolutos fixos (hardcoded) ou falhas não tratadas ao tentar carregar um arquivo ausente.

## Assumptions

- Para atender simultaneamente ao esquema padrão do projeto (`id_venda`, `data_venda`, `cliente`, `produto`, `categoria`, `regiao`, `quantidade`, `preco_unitario` usado nos RFs 01 a 08) e à solicitação da Opção B de usar uma biblioteca geradora de dados mockados/fakes com no mínimo 100 registros, a geração utilizará a biblioteca de dados falsos/mockados (ex.: `Faker`, devidamente fixada nas dependências do projeto) em conjunto com as sementes de aleatoriedade para gerar dados realistas mantendo exatamente os nomes das 8 colunas esperadas pelo restante do pipeline.
- O comportamento do trecho de referência do RF01 que escreve `dados[0]` antes de `dados` (gerando uma linha duplicada deliberada no CSV bruto) é preservado intencionalmente, pois a Constituição do projeto estabelece que `vendas.csv` deve conter inconsistências deliberadas, incluindo registros duplicados, para validação na etapa de limpeza.
- O idioma padrão dos dados, mensagens de console e nomes de colunas é o Português do Brasil (`pt_BR`), utilizando codificação UTF-8 em todas as operações de arquivo.
