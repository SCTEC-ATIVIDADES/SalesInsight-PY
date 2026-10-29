<!--
Sync Impact Report:
- Version change: N/A (template) → 1.0.0
- Modified principles:
  - [PRINCIPLE_1_NAME] → I. Modularização e Separação de Responsabilidades
  - [PRINCIPLE_2_NAME] → II. Processamento Explícito e Estruturas Nativas com Pandas
  - [PRINCIPLE_3_NAME] → III. Desenvolvimento Orientado a Testes (TDD - INEGOCIÁVEL)
  - [PRINCIPLE_4_NAME] → IV. Qualidade, Limpeza de Dados e Tratamento Resiliente de Erros
  - [PRINCIPLE_5_NAME] → V. Padronização de Ambiente com Docker e Rastreabilidade de Saídas
- Added sections:
  - Stack Tecnológica e Restrições Arquiteturais
  - Fluxo de Desenvolvimento, Versionamento e Portões de Qualidade
- Removed sections: None
- Templates requiring updates:
  - .specify/templates/plan-template.md (✅ compatible)
  - .specify/templates/spec-template.md (✅ compatible)
  - .specify/templates/tasks-template.md (✅ compatible)
- Follow-up TODOs: None
-->

# SalesInsight PY Constitution

## Core Principles

### I. Modularização e Separação de Responsabilidades
Toda a lógica de leitura, inspeção, limpeza, transformação, cálculo de métricas, segmentação de
clientes e exportação DEVE residir em funções reutilizáveis dentro de `modulo_vendas.py`, enquanto a
geração sintética/mockada do dataset de vendas DEVE residir em um módulo independente dedicado
(`gerador_dados.py`, podendo ser reexportada por `modulo_vendas.py` para conveniência). Cada
função DEVE possuir nome claro, docstring concisa e assinatura com parâmetros e retornos
explícitos. O ponto de entrada `main.py` DEVE limitar-se a importar e orquestrar o fluxo dentro
de um bloco `if __name__ == "__main__":`, sem conter regras de negócio.

*Justificativa*: Garante reutilização, testabilidade unitária isolada e manutenção simples do
pipeline de dados.

### II. Processamento Explícito e Estruturas Nativas com Pandas
O código DEVE combinar a biblioteca `pandas` e a biblioteca padrão do Python (`csv`, `json`, `os`,
`datetime`, `pathlib`) mantendo a lógica de processamento explícita. O uso de listas, dicionários,
laços `for` e estruturas condicionais DEVE ser claro e legível, evitando expressões opacas de
linha única que ocultem as regras de transformação, agregação e classificação.

*Justificativa*: Preserva a clareza algorítmica e assegura transparência didática e auditabilidade
em cada etapa do pipeline.

### III. Desenvolvimento Orientado a Testes (TDD - INEGOCIÁVEL)
Toda funcionalidade DEVE seguir estritamente o ciclo Vermelho → Verde → Refatoração (Red-Green-
Refactor) utilizando `pytest` em `tests/test_modulo_vendas.py`. Os testes automatizados DEVEM ser
escritos antes da implementação, falhar inicialmente, passar com a implementação mínima necessária
e permanecer verdes após refatorações. A suíte DEVE cobrir leitura, limpeza, cálculos derivados,
agregações, segmentação, exportação e todos os cenários de erro.

*Justificativa*: Previne regressões, documenta o comportamento esperado e valida o tratamento de
dados inconsistentes desde a concepção.

### IV. Qualidade, Limpeza de Dados e Tratamento Resiliente de Erros
O pipeline DEVE tratar de forma determinística e segura: arquivos ausentes, valores nulos ou
vazios, espaços em branco excedentes, tipos numéricos mal formatados, datas inválidas e registros
duplicados. Toda rejeição de registro inválido DEVE ser contabilizada e detalhada por motivo em um
contador estruturado. Falhas de I/O (como arquivo inexistente) DEVEM emitir mensagens claras sem
interromper abruptamente a execução com rastros não tratados.

*Justificativa*: Dados reais de varejo contêm inconsistências; o pipeline deve garantir integridade
analítica nas saídas e rastreabilidade dos descartes.

### V. Padronização de Ambiente com Docker e Rastreabilidade de Saídas
O projeto DEVE prover `Dockerfile`, `docker-compose.yml` e `requirements.txt` com versões fixadas
para garantir execução idêntica de desenvolvimento, testes (`pytest`) e produção (`python main.py`)
em qualquer máquina, montando o código como volume. A exportação DEVE criar automaticamente o
diretório `outputs/` e gerar artefatos estruturados e íntegros (`outputs/metricas_resumo.csv` e
`outputs/estatisticas.json`).

*Justificativa*: Elimina divergências de ambiente ("funciona na minha máquina") e padroniza os
contratos de saída para consumo externo.

## Stack Tecnológica e Restrições Arquiteturais

- **Linguagem e Bibliotecas**: Python 3.11+ com `pandas` e `pytest` com versões fixadas em
  `requirements.txt`, além dos módulos nativos (`csv`, `json`, `os`, `datetime`, `pathlib`).
- **Estrutura de Diretórios Obrigatória**:
  - `gerador_dados.py`: Módulo independente responsável exclusivamente pela geração sintética/mockada do dataset (`gerar_dataset_sintetico`).
  - `modulo_vendas.py`: Funções do pipeline de vendas (leitura, inspeção, limpeza, transformação, agregação, segmentação e exportação).
  - `main.py`: Orquestração principal do fluxo.
  - `vendas.csv`: Dataset de entrada com inconsistências deliberadas para validação.
  - `tests/test_modulo_vendas.py`: Suíte completa de testes automatizados.
  - `outputs/metricas_resumo.csv` e `outputs/estatisticas.json`: Relatórios gerados.
  - `Dockerfile`, `docker-compose.yml`, `requirements.txt` e `README.md`.
- **Regras de Negócio Explícitas**: Limites de faixas de preço (Baixo, Médio, Alto) e de
  segmentação de clientes por gasto acumulado (Bronze, Prata, Ouro) DEVEM estar declarados de
  forma explícita e documentados no código.

## Fluxo de Desenvolvimento, Versionamento e Portões de Qualidade

- **Versionamento Semântico de Commits**: O histórico Git DEVE refletir a evolução lógica do
  desenvolvimento em TDD, utilizando Conventional Commits em português (`test:`, `feat:`, `fix:`,
  `chore:`, `docs:`), registrando os commits de teste antes dos commits de implementação quando
  aplicável.
- **Portões de Qualidade (Quality Gates)**: Nenhuma etapa é considerada concluída sem que todos os
  testes passem via `pytest` e a execução completa via `python main.py` gere os arquivos em
  `outputs/` sem erros, tanto localmente quanto via `docker compose`.
- **Documentação**: O `README.md` DEVE documentar objetivo, pré-requisitos, instalação local,
  execução via Docker Compose, fluxo TDD, justificativa de leitura CSV, estrutura das saídas,
  conceitos aplicados e limitações conhecidas.

## Governance

Esta Constituição governa todas as decisões arquiteturais, especificações, planos e tarefas do
projeto **SalesInsight PY**, prevalecendo sobre práticas informais.

- **Procedimento de Emenda**: Qualquer alteração nesta Constituição DEVE ser documentada com
  justificativa técnica, atualização da data de emenda (`Last Amended`) e revisão de impacto nos
  templates e artefatos dependentes.
- **Política de Versionamento**: Segue Semantic Versioning (`MAJOR.MINOR.PATCH`):
  - `MAJOR`: Remoção ou redefinição incompatível de princípios ou restrições obrigatórias.
  - `MINOR`: Adição de novo princípio, seção ou expansão material das regras de governança.
  - `PATCH`: Refinamentos de redação, correções de digitação ou esclarecimentos sem mudança
    semântica.
- **Revisão de Conformidade**: Todas as especificações (`spec.md`), planos (`plan.md`), tarefas
  (`tasks.md`) e implementações DEVEM ser verificadas contra os cinco princípios fundamentais e os
  portões de qualidade aqui estabelecidos.

**Version**: 1.0.0 | **Ratified**: 2026-10-26 | **Last Amended**: 2026-10-26
