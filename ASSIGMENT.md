# Mini-Projeto Avaliativo

## 1. CONTEXTUALIZAÇÃO

O mercado de Tecnologia e Análise de Dados exige domínio dos fundamentos da linguagem Python: manipulação de estruturas nativas (listas e dicionários), controle de fluxo, modularização do código em funções e manipulação de arquivos.

Neste mini-projeto, você desenvolverá um analisador de dados de vendas estruturado em um módulo de funções reutilizáveis. O objetivo é coletar, limpar, transformar e agregar dados de vendas utilizando estritamente a biblioteca padrão do Python (csv, json), organizando o trabalho com Git.

## 2. DESAFIO

Você atua como Analista de Dados Júnior em uma empresa de varejo e precisa processar um histórico de vendas em formato CSV para gerar um relatório resumido em JSON e CSV.

Você deverá desenvolver o projeto:
> **SalesInsight PY: Pipeline Estruturado de Análise de Dados de Vendas**

A aplicação deverá:

* Ler dados brutos de um arquivo CSV utilizando o módulo nativo `csv`;  
* Limpar dados inconsistentes (remover nulos, converter tipos de dados e remover espaços em branco);  
* Criar novos campos calculados (receita total por item, faixa de preço);  
* Calcular estatísticas e métricas agregadas por categoria e região utilizando dicionários e laços;  
* Segmentar clientes por faixa de gasto acumulado;  
* Exportar os resultados em arquivos CSV e JSON;  
* **Organizar todo o processamento dentro de um módulo Python dedicado** (`modulo_vendas.py`), separando as funções da execução principal (`main.py`).

## 3. RESULTADOS ESPERADOS (ENTREGA)

Ao final do mini-projeto, o estudante ou squad (pequeno grupo de até 03 pessoas) deverá entregar:

* Arquivo principal de execução (main.py).  
* Módulo com as funções (`modulo_vendas.py`).  
* Dataset de entrada (`vendas.csv`).  
* Pasta de relatórios gerados (`outputs/`).  
* Arquivo `README.md` detalhando a execução.  
* Histórico de versionamento local via **Git**.  
* Um vídeo de até 5 minutos demonstrando o funcionamento.  
* Os links submetidos no AVA.

## 4. REQUISITOS DAS TAREFAS

## 4.1. ORGANIZAÇÃO DO PROJETO

A estrutura mínima do projeto deverá ser:

```py
salesinsight-py/
│
├── modulo_vendas.py       # Módulo contendo as funções principais
├── main.py                # Arquivo principal que importa o modulo
├── vendas.csv             # Arquivo com os dados de entrada
├── README.md              # Documentação do projeto
│
└── outputs/               # Pasta gerada com os relatórios exportados
    ├── metricas_resumo.csv
    └── estatisticas.json
```

## 4.2. REQUISITOS FUNCIONAIS

### RF01 – Criar ou Carregar o Dataset de Vendas

O projeto deverá ter um dataset de vendas. O estudante pode **gerar o dataset sinteticamente** no próprio código (recomendado para facilitar a reprodução) ou utilizar um arquivo CSV real.### Código para gerar o dataset no código** (recomendado

```py
import csv
import random

def gerar_dataset_sintetico(caminho_arquivo="vendas.csv", n_registros=100, seed=42):
    random.seed(seed)
    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor", "Teclado", "Mouse"]
    categorias = {"Notebook": "Eletrônicos", "Smartphone": "Celulares", "Tablet": "Celulares",
                  "Monitor": "Eletrônicos", "Teclado": "Acessórios", "Mouse": "Acessórios"}
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    
    cabecalho = ["id_venda", "data_venda", "cliente", "produto", "categoria", "regiao", "quantidade", "preco_unitario"]
    dados = []

    for i in range(1, n_registros + 1):
        prod = random.choice(produtos)
        qtd = str(random.randint(1, 8)) if random.random() > 0.05 else "" # Inserindo nulos
        preco = str(round(random.uniform(100, 3500), 2)) if random.random() > 0.05 else ""
        prod_nome = f"  {prod} " if random.random() < 0.1 else prod

        dados.append([
            i, f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            f"Cliente_{random.randint(1, 30):03d}", prod_nome,
            categorias.get(prod, "Outros"), random.choice(regioes), qtd, preco
        ])

    with open(caminho_arquivo, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(cabecalho)
        writer.writerow(dados[0]) # cabeçalho e dados escriti
        writer.writerows(dados)
    print(f"[OK] Dataset gerado em: {caminho_arquivo}")
```

**Opção B – Usar IA para gerar o CSV**: O estudante pode usar uma IA e solicitar que gere o arquivo CSV, desde que contenha ao menos as colunas: data, produto, categoria, quantidade, preço e região. O mínimo de registros é 100.

### RF02 – Inspecionar e Descrever os Dados

Criar uma função no módulo para exibir a quantidade total de registros carregados e verificar linhas com dados incompletos ou nulos.

**Exemplo** de função:

```py
def inspecionar_dados(dados):
    print("\n=== INSPEÇÃO INICIAL DOS DADOS ===")
    print(f"Total de registros carregados: {len(dados)}")
    if dados:
        print(f"Campos disponíveis: {list(dados[0].keys())}")
        print(f"Exemplo do primeiro registro: {dados[0]}")
```

### RF03 – Limpar e Tratar os Dados

A função deve ler a lista de dicionários, remover espaços extras nas strings (`.strip()`), ignorar/filtrar registros com valores vazios ou inválidos para `quantidade` e `preco_unitario`, e converter esses campos para `int` e `float`.

Exemplo:

```py
def limpar_dados(dados_brutos):
    dados_limpos = []
    removidos = 0

    for lin in dados_brutos:
        # Tratamento de espaços
        prod = lin["produto"].strip()
        cat = lin["categoria"].strip()
        reg = lin["regiao"].strip()
        cli = lin["cliente"].strip()

        # Validação de nulos/vazios
        if not lin["quantidade"] or not lin["preco_unitario"]:
            removidos += 1
            continue

        try:
            qtd = int(lin["quantidade"])
            preco = float(lin["preco_unitario"])
            dados_limpos.append({
                "id_venda": int(lin["id_venda"]),
                "data_venda": lin["data_venda"].strip(),
                "cliente": cli,
                "produto": prod,
                "categoria": cat,
                "regiao": reg,
                "quantidade": qtd,
                "preco_unitario": preco
            })
        except ValueError:
            removidos += 1

    print(f"\n=== RELATÓRIO DE LIMPEZA ===")
    print(f"Registros Válidos: {len(dados_limpos)} | Registros Removidos: {removidos}")
    return dados_limpos
```

### RF04 – Criar Campos Derivados

Adicionar a cada registro os campos:

* `receita_total`: resultado de `quantidade * preco_unitario`.  
* `faixa_preco`: "Baixo" (\< R\$ 500), "Médio" (entre R\$ 500 e R\$ 2000\) e "Alto" (\> R\$ 2000).

Exemplo:

```py
def criar_campos_derivados(dados):
    for item in dados:
        receita = round(item["quantidade"] * item["preco_unitario"], 2)
        item["receita_total"] = receita
        
        if receita < 500:
            item["faixa_preco"] = "Baixo"
        elif receita <= 2000:
            item["faixa_preco"] = "Médio"
        else:
            item["faixa_preco"] = "Alto"
    return dados
```

### RF05 – Calcular Métricas Agregadas

Desenvolver funções agregadoras utilizando dicionários para calcular:

* Receita total por Categoria.  
* Receita total por Região.  
* Total geral de vendas da empresa.

Exemplo de implementação:

```py
def calcular_metricas(dados):
    receita_categoria = {}
    receita_regiao = {}
    total_geral = 0.0

    for item in dados:
        cat = item["categoria"]
        reg = item["regiao"]
        rec = item["receita_total"]

        receita_categoria[cat] = round(receita_categoria.get(cat, 0.0) + rec, 2)
        receita_regiao[reg] = round(receita_regiao.get(reg, 0.0) + rec, 2)
        total_geral += rec

    return {
        "total_geral": round(total_geral, 2),
        "por_categoria": receita_categoria,
        "por_regiao": receita_regiao
    }
```

### RF06 – Segmentar Clientes por Nível de Gasto

Calcular o total de compras por cliente e classificá-los em categorias:

| Gasto Total | Segmento |
| :---- | :---- |
| Abaixo de R\$ 3.000 | Bronze |
| R\$ 3.000 a R\$ 8.000 | Prata |
| Acima de R\$ 8.000 | Ouro |

Exemplo:

```py
def segmentar_clientes(dados):
    gastos_cliente = {}
    for item in dados:
        cli = item["cliente"]
        gastos_cliente[cli] = gastos_cliente.get(cli, 0.0) + item["receita_total"]

    segmentos = {}
    for cli, total in gastos_cliente.items():
        if total > 8000:
            cat = "Ouro"
        elif total >= 3000:
            cat = "Prata"
        else:
            cat = "Bronze"
        segmentos[cli] = {"total_gasto": round(total, 2), "segmento": cat}

    return segmentos
```

### RF07 – Ler e Escrever Arquivos (CSV e JSON)

O código deve ler dados de entrada via `csv.DictReader` e exportar resultados usando os módulos nativos `csv` e `json`.

Exemplo:

```py
import json
import os

def carregar_csv(caminho_arquivo):
    dados = []
    with open(caminho_arquivo, mode="r", encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            dados.append(linha)
    return dados

def exportar_resultados(metricas, clientes, pasta_saida="outputs"):
    os.makedirs(pasta_saida, exist_ok=True)
    
    # Exportar JSON com métricas gerais
    caminho_json = os.path.join(pasta_saida, "estatisticas.json")
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump({"metricas_gerais": metricas, "clientes": clientes}, f, indent=4, ensure_ascii=False)
    print(f"[OK] Arquivo JSON exportado em: {caminho_json}")

    # Exportar CSV com resumo de categorias
    caminho_csv = os.path.join(pasta_saida, "metricas_resumo.csv")
    with open(caminho_csv, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["Categoria", "Receita Total"])
        for cat, rec in metricas["por_categoria"].items():
            escritor.writerow([cat, rec])
    print(f"[OK] Arquivo CSV exportado em: {caminho_csv}")
```

### RF08 – Executar o Pipeline Completo (Ponto de Entrada)

No arquivo `main.py`, importar as funções do módulo `modulo_vendas.py` e executar o fluxo de ponta a ponta.

*Exemplo do arquivo `main.py`:*

```py
import os
import modulo_vendas as mv

def main():
    print("=" * 60)
    print(" SALESINSIGHT PY - Pipeline de Processamento com Python Nativo")
    print("=" * 60)

    arquivo_dados = "vendas.csv"

    # 1. Gerar dataset sintético se não existir
    if not os.path.exists(arquivo_dados):
        mv.gerar_dataset_sintetico(arquivo_dados, n_registros=150)

    # 2. Leitura
    dados_brutos = mv.carregar_csv(arquivo_dados)
    mv.inspecionar_dados(dados_brutos)

    # 3. Limpeza e Transformação
    dados_limpos = mv.limpar_dados(dados_brutos)
    dados_transformados = mv.criar_campos_derivados(dados_limpos)

    # 4. Uso de Função de Ordem Superior com Lambda (exemplo)
    dados_com_tag = mv.processar_transformacao(
        dados_transformados, 
        lambda x: {**x, "processado": True}
    )

    # 5. Métricas e Segmentação
    metricas = mv.calcular_metricas(dados_com_tag)
    segmentos = mv.segmentar_clientes(dados_com_tag)
    top_clientes = mv.obter_top_clientes(segmentos, top_n=5)

    # 6. Exibição de Resultados
    print("\n=== RESUMO EXECUTIVO ===")
    print(f"Receita Total da Empresa: R$ {metricas['total_geral']:,.2f}")
    print("\nTop 5 Clientes Ouro/Prata:")
    for cli, info in top_clientes:
        print(f"  - {cli}: R$ {info['total_gasto']:,.2f} ({info['segmento']})")

    # 7. Exportação dos Arquivos
    mv.exportar_resultados(metricas, segmentos)

    print("\n[CONCLUÍDO] Pipeline executado com sucesso!")

if __name__ == "__main__":
    main()
```

## 4.3. REQUISITOS TÉCNICOS

| Conteúdo | Obrigatório? | Como Demonstrar |
| :---- | :---- | :---- |
| **Modularização (**.py**)** | **Sim** | Funções em modulo\_vendas.py importadas no main.py |
| **Manipulação de Arquivos** | **Sim** | Leitura e escrita nativa com csv e json |
| **Estruturas Nativas** | **Sim** | Uso explícito de list, dict, laços for e condicionais |
| **Versionamento com Git** | **Sim** | Histórico de commits locais na pasta do projeto |

## 4.4. VERSIONAMENTO COM GIT

O projeto deve utilizar versionamento local com **Git**, demonstrando uma sequência de commits que representem a evolução lógica do desenvolvimento.

Comandos básicos esperados no fluxo de trabalho:

1. `git init` (inicialização do repositório no diretório do projeto)  
2. `git status` (verificação das alterações)  
3. `git add .` (adicionando arquivos ao staging)  
4. `git commit -m "mensagem descritiva"` (registro de alterações)  
5. `git log` (visualização do histórico de alterações)

**Commits mínimos:**

* mínimo de 5 commits

**Exemplos de mensagens de commit:**

```py
feat: cria estrutura inicial do projeto e arquivo salesinsight.py
feat: adiciona função de geração e leitura do dataset CSV
feat: implementa limpeza de dados e tratamento de nulos
feat: implementa exportação de CSV e JSON
docs: atualiza readme com instruções de execução e conceitos
fix: corrige conversão de datas inválidas
```

## 4.6. GRAVAÇÃO DE VÍDEO

Apresentação técnica individual ou em grupo de até **5 minutos**:

* Mostrar a estrutura dos arquivos (`main.py` e `modulo_vendas.py`).  
* Executar a aplicação via terminal.  
* Exibir os arquivos gerados na pasta `outputs/`.  
* Mostrar o repositório local Git (`git log`).

## 5. CRITÉRIOS DE AVALIAÇÃO

| Organização do projeto |  |  |  |  |
| :---: | ----- | ----- | ----- | ----- |

| Nº | Critério de Avaliação | 0 | 0,50 | 1,00 |
| :---- | :---: | :---: | :---: | :---: |
| **01** | **Versionamento com branches e commits** | O repositório do projeto não apresenta branches e commits. | O repositório do projeto apresenta parte das branches e commits distintos e nomeadas padronizadamente para cada funcionalidade desenvolvida. | O repositório do projeto apresenta branches e commits distintos e nomeadas padronizadamente para cada funcionalidade desenvolvida. |
| **02** | **Organização dos arquivos no repositório e Readme** | O repositório do projeto não apresenta os arquivos estruturados conforme as instruções.  | O repositório do projeto apresenta parte dos arquivos estruturados conforme as instruções, ou não possui o Readme completo.  | O repositório do projeto apresenta os arquivos estruturados conforme as instruções e apresenta o Readme explicando o projeto. |

| Apresentação do Projeto |  |  |  |  |
| :---: | ----- | ----- | ----- | ----- |

| Nº | Critério de Avaliação | 0,00 | 1,00 | 2,00 |
| :---: | ----- | :---: | :---: | :---: |
| **03** | **Gravação de vídeo** | Não gravou o vídeo de apresentação. | Gravou o vídeo de apresentação, mas não apresentou todos os requisitos do ítem 4.6. | O vídeo apresentou todos os requisitos do ítem 4.6. |

| Desenvolvimento do Projeto  |  |  |  |  |
| :---: | ----- | ----- | ----- | ----- |

| Nº | Critério de Avaliação | 0,00 | 0,50 | 0,75 |
| :---: | :---- | :---: | :---: | :---: |
| **04** | **RF01 – Dataset de Vendas** | Não implementou a rotina de leitura/criação do dataset de vendas ou a função apresenta erros de execução que impedem o acesso aos dados.  | O código realiza o carregamento ou criação do dataset de vendas, porém apresenta dependência de caminhos absolutos (hardcoded), falhas no tratamento do caminho do arquivo de origem ou disponibiliza a estrutura de dados com inconsistências pontuais para as etapas seguintes.  | O projeto apresenta a função ou rotina de carregamento/criação do conjunto de dados de vendas (dataset) estruturada e funcional, garantindo o acesso correto à fonte de dados e a disponibilização da estrutura para as etapas posteriores de análise.  |
| **05** | **RF02 – Inspecção e Descrição dos Dados** | Não desenvolveu a função de inspeção de dados ou a rotina não é capaz de identificar registros nulos/incompletos e a quantidade de linhas da base.  | A função de inspeção exibe o total de registros ou identifica linhas incompletas/nulas, mas falha em entregar ambos os diagnósticos de forma consolidada ou apresenta divergências contábeis na contagem de nulos.  | O módulo contém função dedicada à inspeção do dataset, capaz de exibir o total de registros carregados e mapear a presença de linhas com dados incompletos ou nulos no conjunto de dados.  |
| **06** | **RF03 – Limpeza e tratamento de Dados** | Não aplicou as rotinas de tratamento e conversão de dados, mantendo a base bruta com inconsistências, tipos incorretos ou caracteres sobressalentes.  | Executa parcialmente a higienização da base (ex.: realiza a remoção de espaços em branco com `.strip()`, mas falha em converter corretamente os tipos numéricos para `int`/`float` ou deixa passar registros vazios/inválidos).  | Aplicou técnicas de limpeza e tratamento de dados em Python, automatizando a remoção de caracteres sobressalentes, a filtragem de inconsistências numéricas e a conversão explícita de tipos de dados para assegurar a qualidade da base.  |
| **07** | **RF04 – Criação de Campos Derivados**  | Não adicionou os campos requeridos no RF04 aos registros do dataset.  | Incorporou apenas parte dos novos campos exigidos no RF04 aos registros ou apresentou falhas no cálculo/lógica de derivação das novas colunas.  | Adicionou a cada registro os campos solicitados no RF04 |
| **08** | **RF05 – Cálculo de Métricas Agregadas** | Não construiu as funções de agregação com dicionários ou os valores calculados de receita e faturamento apresentam erros de lógica divergentes da base.  | Desenvolveu funções de agregação com dicionários, mas calcula apenas parte dos indicadores solicitados ou apresenta inconsistências pontuais nos somatórios de faturamento.  | As funções de agregação utilizam estruturas de dicionários para processar o conjunto de dados de vendas, calculando e retornando de forma precisa a receita total por categoria, a receita total por região e o faturamento global da empresa para suporte à tomada de decisão.  |
| **09** | **RF06 – Segmentação de Clientes por Nível de Gasto** | Não desenvolveu a rotina de cálculo por cliente ou não aplicou a classificação por faixas de gasto conforme o RF06.  | Calcula o volume total acumulado por cliente, porém apresenta erros nas regras condicionais de enquadramento das categorias/faixas de gasto | O módulo de processamento de dados calcula o volume total de compras acumulado por cliente e executa a segmentação em categorias, conforme estipulado no RF06 |
| **10** | **RF07 - Leitura e Escrita de Arquivos** | Não implementou a leitura via `csv.DictReader` ou falhou na exportação dos arquivos em formato CSV e JSON.  | Realiza a leitura e exportação dos dados, porém recorre a métodos de leitura sem `csv.DictReader`, exporta em apenas um dos formatos exigidos (somente CSV ou somente JSON) ou gera arquivos com falhas de formatação/estrutura.  | O módulo de persistência de dados realiza a leitura parametrizada da base de entrada utilizando `csv.DictReader` e exporta os resultados processados em formatos estruturados CSV e JSON por meio dos módulos nativos do Python, garantindo a integridade e a correta formatação dos arquivos gerados.  |
| **11** | **RF08 – Execução do Pipeline Completo**   | Não estruturou o ponto de entrada no `main.py`, não realizou a modularização dos arquivos ou o pipeline quebra ao ser executado, impedindo o fluxo de ponta a ponta.  | O arquivo `main.py` importa o módulo e executa partes do fluxo, porém a execução é interrompida por exceções durante a passagem de parâmetros entre as etapas ou exige intervenção manual no código para concluir o pipeline.  | O arquivo principal (`main.py`) atua como ponto de entrada da aplicação, importando adequadamente as funções do módulo `modulo_vendas.py` e orquestrando a execução contínua e sem falhas do pipeline de dados de ponta a ponta.  |

## 6. CHECKLIST FINAL DE ENTREGA

Antes de enviar no AVA, confira:

* [ ] Arquivo `modulo_vendas.py` criado com todas as funções de suporte.
* [ ] Arquivo `main.py` executando o pipeline de forma automatizada.
* [ ] Leitura do CSV e geração de saídas em CSV e JSON na pasta `outputs/`.
* [ ] Histórico de versionamento gerado com `git commit`.
* [ ] Arquivo `README.md` preenchido conforme o modelo.
* [ ] Vídeo demonstrativo gravado

## 7. MODELO DE README.md (SUGESTÃO)

```markdown
## SalesInsight PY - Pipeline de Análise de Dados de Vendas

Proposta de pipeline simples e modularizado para tratamento, transformação e agregação de dados de vendas utilizando recursos nativos da linguagem Python.

## 📁 Estrutura do Projeto

- `main.py`: Ponto de entrada do projeto.
- `modulo_vendas.py`: Módulo contendo as funções de leitura, tratamento e exportação.
- `vendas.csv`: Dataset sintético de vendas.
- `outputs/`: Diretório contendo os relatórios finais em CSV e JSON.

## 🚀 Como Executar

1. Certifique-se de ter o Python 3 instalado.
2. Clone ou descompacte o repositório.
3. No terminal, execute o comando:
   python main.py
```
