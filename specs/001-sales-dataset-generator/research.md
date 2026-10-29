# Phase 0 Research: RF01 – Criar ou Carregar o Dataset de Vendas

**Feature**: `001-sales-dataset-generator`  
**Date**: 2026-10-26

## 1. Biblioteca de Geração de Dados Mockados/Fakes, Determinismo e Módulo Independente

- **Decision**: Isolar a geração de dados no módulo independente `gerador_dados.py` utilizando a biblioteca `Faker` (`Faker('pt_BR')` com `Faker.seed(seed)` e `instancia.seed_instance(seed)`) combinada com `random.seed(seed)` da biblioteca padrão do Python para geração de registros de vendas realistas e 100% determinísticos (com reexportação de `gerar_dataset_sintetico` em `modulo_vendas.py` por compatibilidade).
- **Rationale**:
  - A especificação da tarefa solicita na Opção B o uso de uma biblioteca para gerar dados reais/mockados/fakes com no mínimo 100 registros, mantendo o contrato estrutural do RF01 (`id_venda`, `data_venda`, `cliente`, `produto`, `categoria`, `regiao`, `quantidade`, `preco_unitario`).
  - `Faker` é o padrão de mercado em Python para geração de dados sintéticos/mockados localizados (`pt_BR`), permitindo gerar nomes de clientes/identificadores e datas realistas em 2024 de forma determinística quando semeado com `seed_instance(seed)`.
  - O módulo nativo `random` semeado com a mesma `seed` controla a seleção do catálogo de produtos/categorias/regiões e as probabilidades exatas de injeção de ruídos (5% `quantidade` vazia, 5% `preco_unitario` vazio, 10% espaços extras em `produto`, além da duplicação deliberada de `dados[0]`).
- **Alternatives considered**:
  - *Apenas `random` nativo*: Atende ao código base do enunciado, mas não utiliza uma biblioteca dedicada de dados mockados/fakes conforme solicitado pelo usuário na descrição da feature.
  - *`Mimesis` ou `Factory Boy`*: `Mimesis` é rápido, porém `Faker` possui suporte mais amplo, documentação consolidada em projetos acadêmicos/corporativos Python e controle simples de instância (`seed_instance`).

## 2. Leitura e Escrita de CSV (Compatibilidade entre `csv` Nativo e `pandas`)

- **Decision**: Implementar a escrita em `gerar_dataset_sintetico` com `csv.writer` (módulo nativo `csv`, `encoding="utf-8"`, `newline=""`) e a leitura em `carregar_csv` com `csv.DictReader`, utilizando `pandas` complementarmente no módulo quando aplicável às verificações/estruturas tabulares previstas na Constituição.
- **Rationale**:
  - O Critério de Avaliação nº 10 (`ASSIGMENT.md`) exige explicitamente que a leitura parametrizada da base de entrada utilize `csv.DictReader` e os módulos nativos `csv` e `json`.
  - O Princípio II da Constituição (`constitution.md`) determina combinar `pandas` e a biblioteca padrão (`csv`, `json`, `os`, `datetime`, `pathlib`) mantendo a lógica explícita com listas, dicionários e laços `for`.
  - Retornar `list[dict[str, str]]` a partir de `csv.DictReader` garante compatibilidade direta com `inspecionar_dados(dados_brutos)` e `limpar_dados(dados_brutos)` nos RFs subsequentes.
- **Alternatives considered**:
  - *Leitura exclusivamente via `pandas.read_csv()`*: Violará o Critério de Avaliação nº 10 da rubrica que penaliza implementações que não utilizam `csv.DictReader`.
  - *Caminhos fixos (hardcoded)*: Rejeitado pelo Critério de Avaliação nº 04 e FR-008; todas as funções recebem `caminho_arquivo: str | Path = "vendas.csv"` usando `pathlib.Path` / `os.path`.

## 3. Injeção Controlada de Inconsistências para Validação do Pipeline

- **Decision**: Manter na geração do dataset a injeção determinística dos 4 tipos de ruídos exigidos pela Constituição (Princípio IV) e pelo enunciado:
  1. `quantidade` vazia (`""`) com ~5% de probabilidade (`random.random() <= 0.05`);
  2. `preco_unitario` vazio (`""`) com ~5% de probabilidade (`random.random() <= 0.05`);
  3. Espaços em branco sobressalentes no campo `produto` (`f"  {prod} "`) com ~10% de probabilidade (`random.random() < 0.10`);
  4. Linha duplicada deliberada escrevendo `dados[0]` antes de `writer.writerows(dados)` (conforme o trecho de referência do RF01).
- **Rationale**: Garante que `vendas.csv` exercite todas as regras de inspeção (RF02) e limpeza/deduplicação (RF03) sem depender de edição manual do arquivo CSV.
- **Alternatives considered**:
  - *Gerar apenas dados 100% limpos*: Impediria a validação real dos contadores de rejeição e limpeza exigidos pelo Princípio IV da Constituição e pelos RFs 02 e 03.

## 4. Tratamento Resiliente de Erros de I/O

- **Decision**: Em `carregar_csv(caminho_arquivo="vendas.csv")`, verificar a existência e acessibilidade do arquivo via `Path(caminho_arquivo)` dentro de bloco `try...except (FileNotFoundError, OSError)`, exibindo mensagem clara (`[ERRO] Arquivo não encontrado: ...`) e retornando lista vazia `[]` sem lançar traceback não tratado. Em `gerar_dataset_sintetico`, criar diretórios pais automaticamente (`Path(caminho_arquivo).parent.mkdir(parents=True, exist_ok=True)`).
- **Rationale**: Atende integralmente ao Princípio IV da Constituição ("Falhas de I/O (como arquivo inexistente) DEVEM emitir mensagens claras sem interromper abruptamente a execução com rastros não tratados") e aos cenários de borda do RF01.
- **Alternatives considered**:
  - *Deixar `FileNotFoundError` estourar sem tratamento*: Viola o Princípio IV da Constituição e o Critério de Avaliação nº 04.

## 5. Isolamento de Ambiente Local com `venv` e Complementaridade com Docker

- **Decision**: Adotar ambiente virtual nativo do Python (`python3 -m venv .venv`) como padrão oficial para desenvolvimento e execução local isolada, mantendo o `Dockerfile` e `docker-compose.yml` para execução containerizada e excluindo `.venv/` em `.gitignore` e `.dockerignore` (conforme FR-010).
- **Rationale**: Evita conflitos com pacotes globais do sistema operacional (PEP 668 / `externally-managed-environment` em distribuições Linux modernas com Python 3.11+), garante que as mesmas versões fixadas em `requirements.txt` sejam utilizadas tanto localmente quanto no container Docker e preserva a limpeza do repositório e do contexto de build.
- **Alternatives considered**:
  - *Instalação direta no Python global do sistema (`pip install` sem `venv`)*: Causa conflitos de dependências entre projetos e falha em sistemas com proteção PEP 668.
  - *Substituir Docker exclusivamente por `venv`*: Violará o Princípio V da Constituição que exige `Dockerfile` e `docker-compose.yml`.
