# Quickstart & Validation Guide: RF02 – Inspecionar e Descrever os Dados

**Feature**: `002-data-inspection`
**Date**: 2026-10-28

## 1. Pré-requisitos

- **Python**: 3.11+ (ambiente virtual `.venv` ativo) ou **Docker Compose**
- **Dependências instaladas**: `pip install -r requirements.txt`

## 2. Cenários de Validação Executáveis

### Cenário 1: Executar a Suíte de Testes Automatizados (TDD / Pytest)

Valida a exibição do total de registros carregados, campos disponíveis, exemplo do primeiro registro, contagem de linhas com dados incompletos/nulos, comportamento seguro com lista vazia (`[]`) e imutabilidade dos dados brutos.

```bash
.venv/bin/pytest tests/test_modulo_vendas.py -v
```

**Resultado Esperado**:
- Todos os testes de RF01 e RF02 passam (`PASSED`).

---

### Cenário 2: Executar a Inspeção via Fluxo Principal (`main.py`)

```bash
.venv/bin/python main.py
```

**Resultado Esperado**:
- Carrega `vendas.csv` (gerando-o caso não exista) e exibe no console a seção `=== INSPEÇÃO INICIAL DOS DADOS ===` com:
  - `Total de registros carregados: 151`
  - `Campos disponíveis: ['id_venda', 'data_venda', 'cliente', 'produto', 'categoria', 'regiao', 'quantidade', 'preco_unitario']`
  - `Exemplo do primeiro registro: {...}`
  - `Registros com dados incompletos ou nulos: <N>` (maior que 0 devido aos ruídos controlados do dataset sintético)
  - `Valores nulos/vazios por campo: {...}`

---

### Cenário 3: Validar Comportamento com Lista Vazia

```bash
.venv/bin/python -c "import modulo_vendas as mv; res = mv.inspecionar_dados([]); assert res['total_registros'] == 0 and res['registros_incompletos'] == 0"
```

**Resultado Esperado**:
- Exibe `Total de registros carregados: 0` sem lançar `IndexError` e retorna resumo zerado.

## 3. Referências

- **Modelo de Dados**: [`data-model.md`](./data-model.md)
- **Contrato de Interface**: [`contracts/inspection-contract.md`](./contracts/inspection-contract.md)
- **Especificação da Feature**: [`spec.md`](./spec.md)
