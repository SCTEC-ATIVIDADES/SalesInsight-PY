# Data Model: RF02 – Inspecionar e Descrever os Dados

**Feature**: `002-data-inspection`
**Date**: 2026-10-28

## 1. Entidades

### 1.1. `RegistroVendaBruto` (Entrada da Inspeção)

Representa cada linha carregada por `carregar_csv` (ou fornecida em memória nos testes) como um dicionário mapeando o nome da coluna ao valor bruto lido.

| Campo | Tipo em Memória | Estado Esperado na Inspeção (RF02) |
|-------|-----------------|------------------------------------|
| `id_venda` | `str \| None` | Preenchido (ex.: `"1"`), podendo repetir em caso de duplicata bruta |
| `data_venda` | `str \| None` | Data ISO `YYYY-MM-DD` (ex.: `"2024-05-14"`) |
| `cliente` | `str \| None` | Identificador do cliente |
| `produto` | `str \| None` | Nome do produto (podendo conter espaços extras como `"  Mouse "`) |
| `categoria` | `str \| None` | Categoria do produto |
| `regiao` | `str \| None` | Região geográfica |
| `quantidade` | `str \| None` | Inteiro em string (`"1"`..`"8"`) ou vazio/nulo (`""`, `"   "`, `None`) |
| `preco_unitario` | `str \| None` | Float em string (`"100.0"`..`"3500.0"`) ou vazio/nulo (`""`, `"   "`, `None`) |

---

### 1.2. `ResumoInspecaoDados` (Saída Estruturada de `inspecionar_dados`)

Dicionário retornado por `inspecionar_dados(dados)` sintetizando o diagnóstico estrutural e de completude da coleção inspecionada.

| Chave | Tipo | Descrição | Valor quando `dados == []` |
|-------|------|-----------|----------------------------|
| `total_registros` | `int` | Quantidade total de registros na coleção (`len(dados)`) | `0` |
| `campos` | `list[str]` | Lista de campos disponíveis na ordem das chaves do primeiro registro | `[]` |
| `primeiro_registro` | `dict[str, str \| None] \| None` | Referência/cópia superficial do primeiro registro da coleção | `None` |
| `registros_incompletos` | `int` | Total de linhas que possuem ao menos um campo vazio (`""`), só com espaços ou `None` | `0` |
| `nulos_por_campo` | `dict[str, int]` | Contagem de ocorrências vazias/nulas para cada campo disponível | `{}` |

---

## 2. Fluxo de Dados e Transformação Diagnóstica

```text
[list[dict[str, str]]] (dados_brutos carregados por carregar_csv)
       │
       ▼  inspecionar_dados(dados_brutos)  [Somente-leitura / Zero mutação]
       ├──► Console (stdout):
       │      === INSPEÇÃO INICIAL DOS DADOS ===
       │      Total de registros carregados: <N>
       │      Campos disponíveis: [...]
       │      Exemplo do primeiro registro: {...}
       │      Registros com dados incompletos ou nulos: <M>
       │      Valores nulos/vazios por campo: {...}
       │
       └──► Retorno: ResumoInspecaoDados (dict[str, Any])
```

## 3. Regras de Validação e Invariantes (Escopo RF02)

1. **Imutabilidade da Entrada**: A coleção `dados` e cada dicionário interno não podem sofrer qualquer alteração durante `inspecionar_dados(dados)`.
2. **Definição de Valor Incompleto/Nulo**: Um valor `v` é considerado incompleto/nulo se e somente se `v is None` ou `(isinstance(v, str) and v.strip() == "")`.
3. **Não-Negatividade e Limites**:
   - `0 <= registros_incompletos <= total_registros`
   - Para cada campo `c` em `campos`: `0 <= nulos_por_campo[c] <= total_registros`
4. **Segurança em Coleção Vazia**: Se `len(dados) == 0`, nenhuma tentativa de acesso a `dados[0]` é realizada.
