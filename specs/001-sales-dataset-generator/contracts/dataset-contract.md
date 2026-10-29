# Contract: Interface do Módulo e Esquema CSV (RF01)

**Feature**: `001-sales-dataset-generator`
**Modules**: `gerador_dados.py` (geração independente) e `modulo_vendas.py` (leitura e reexportação)
**Date**: 2026-10-26

## 1. Contratos de Funções Públicas (`gerador_dados.py` e `modulo_vendas.py`)

### 1.1. `gerar_dataset_sintetico` (`gerador_dados.py`, reexportada em `modulo_vendas.py`)

```python
def gerar_dataset_sintetico(
    caminho_arquivo: str | os.PathLike[str] = "vendas.csv",
    n_registros: int = 100,
    seed: int = 42,
) -> str:
```

- **Responsabilidade**: Gerar um arquivo CSV de vendas com dados sintéticos/mockados realistas (usando `Faker('pt_BR')` e `random` semeados com `seed`) e inconsistências deliberadas controladas.
- **Parâmetros**:
  - `caminho_arquivo` (`str | os.PathLike[str]`, padrão `"vendas.csv"`): Caminho relativo ou parametrizado onde o arquivo CSV será gravado. Cria diretórios pais automaticamente caso não existam.
  - `n_registros` (`int`, padrão `100`): Quantidade base de registros únicos a gerar (deve ser `>= 1`; padrão `100` atende ao mínimo do projeto).
  - `seed` (`int`, padrão `42`): Semente para `random.seed(seed)` e `Faker.seed_instance(seed)` garantindo reprodutibilidade determinística.
- **Efeitos Colaterais**:
  - Cria/sobrescreve o arquivo CSV em `caminho_arquivo` codificado em `utf-8` com `newline=""`.
  - Escreve a linha de cabeçalho, seguida de `dados[0]` (duplicata intencional para teste de limpeza) e das `n_registros` linhas de `dados`.
  - Imprime no stdout: `[OK] Dataset gerado em: {caminho_arquivo}`.
- **Retorno**:
  - `str`: Caminho do arquivo gerado convertido para string.
- **Exceções**:
  - `ValueError`: Se `n_registros < 1`.

---

### 1.2. `carregar_csv`

```python
def carregar_csv(
    caminho_arquivo: str | os.PathLike[str] = "vendas.csv",
) -> list[dict[str, str]]:
```

- **Responsabilidade**: Ler um arquivo CSV de vendas utilizando `csv.DictReader` e retornar a lista de registros brutos em memória.
- **Parâmetros**:
  - `caminho_arquivo` (`str | os.PathLike[str]`, padrão `"vendas.csv"`): Caminho para o arquivo CSV de entrada.
- **Comportamento**:
  - Abre o arquivo em modo leitura (`mode="r"`, `encoding="utf-8"`, `newline=""`).
  - Itera explicitamente sobre `csv.DictReader(f)` adicionando cada linha como `dict[str, str]` em uma lista.
  - Caso o arquivo não exista ou ocorra falha de leitura (`FileNotFoundError`, `OSError`), captura a exceção, exibe mensagem clara (`[ERRO] Arquivo não encontrado: {caminho_arquivo}`) e retorna `[]`.
- **Retorno**:
  - `list[dict[str, str]]`: Lista de dicionários representando os registros brutos lidos do CSV.

---

## 2. Contrato do Arquivo `vendas.csv`

- **Codificação**: `UTF-8`
- **Separador**: `,` (vírgula padrão CSV)
- **Terminador de Linha**: `\n` / padrão `csv.writer` com `newline=""`
- **Cabeçalho Obrigatório (Linha 1)**:
  ```csv
  id_venda,data_venda,cliente,produto,categoria,regiao,quantidade,preco_unitario
  ```
- **Exemplo de Linhas Geradas**:
  ```csv
  id_venda,data_venda,cliente,produto,categoria,regiao,quantidade,preco_unitario
  1,2024-05-14,Cliente_012 - Mariana Silva,Notebook,Eletrônicos,Sudeste,3,2450.75
  1,2024-05-14,Cliente_012 - Mariana Silva,Notebook,Eletrônicos,Sudeste,3,2450.75
  2,2024-11-03,Cliente_004 - Carlos Souza,  Mouse ,Acessórios,Sul,,189.9
  3,2024-02-21,Cliente_019 - Fernanda Lima,Smartphone,Celulares,Nordeste,2,
  ```
