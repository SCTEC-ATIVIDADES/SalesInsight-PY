# Quickstart & Validation Guide: RF01 – Criar ou Carregar o Dataset de Vendas

**Feature**: `001-sales-dataset-generator`  
**Date**: 2026-10-26

## 1. Pré-requisitos

- **Python**: 3.11+ (local) ou **Docker** + **Docker Compose**
- **Dependências** (`requirements.txt`):
  - `pandas`
  - `pytest`
  - `Faker`

### Instalação Local

```bash
pip install -r requirements.txt
```

## 2. Cenários de Validação Executáveis

### Cenário 1: Executar a Suíte de Testes Automatizados (TDD / Pytest)

Valida a geração determinística do dataset (`gerar_dataset_sintetico`), presença das 8 colunas obrigatórias, mínimo de 100 registros, presença de ruídos controlados (nulos, espaços extras e duplicata), carregamento via `carregar_csv` (`csv.DictReader`) e tratamento seguro de arquivo inexistente.

```bash
pytest tests/test_modulo_vendas.py -v
```

**Resultado Esperado**:
- Todos os testes do RF01 passam (`PASSED`).

---

### Cenário 2: Gerar e Carregar o Dataset via Linha de Comando

```bash
python -c "import gerador_dados as gd, modulo_vendas as mv; gd.gerar_dataset_sintetico('vendas.csv', n_registros=100, seed=42); dados = mv.carregar_csv('vendas.csv'); print('Registros lidos:', len(dados)); print('Colunas:', list(dados[0].keys()))"
```

**Resultado Esperado**:
- Mensagem `[OK] Dataset gerado em: vendas.csv`.
- `Registros lidos: 101` (100 registros gerados + 1 registro duplicado deliberado conforme especificação do RF01).
- `Colunas: ['id_venda', 'data_venda', 'cliente', 'produto', 'categoria', 'regiao', 'quantidade', 'preco_unitario']`.

---

### Cenário 3: Validar Tratamento Resiliente de Arquivo Ausente

```bash
python -c "import modulo_vendas as mv; dados = mv.carregar_csv('arquivo_inexistente.csv'); assert dados == []; print('Retorno seguro:', dados)"
```

**Resultado Esperado**:
- Mensagem clara informando que o arquivo não foi encontrado, sem traceback não tratado.
- `Retorno seguro: []`.

---

### Cenário 4: Execução Padronizada via Docker Compose

```bash
docker compose run --rm app pytest
docker compose up --build
```

**Resultado Esperado**:
- Os testes e o ponto de entrada executam no container com o mesmo comportamento do ambiente local.

## 3. Referências

- **Modelo de Dados**: [`data-model.md`](./data-model.md)
- **Contrato de Funções e Esquema CSV**: [`contracts/dataset-contract.md`](./contracts/dataset-contract.md)
- **Especificação da Feature**: [`spec.md`](./spec.md)
