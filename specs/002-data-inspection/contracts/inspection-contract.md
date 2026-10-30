# Contract: Interface de Inspeção de Dados (RF02)

**Feature**: `002-data-inspection`
**Modules**: `modulo_vendas.py` (implementação) e `main.py` (orquestração)
**Date**: 2026-10-28

## 1. Contrato de Função Pública (`modulo_vendas.py`)

### 1.1. `inspecionar_dados`

```python
def inspecionar_dados(
    dados: list[dict[str, str | None]],
) -> dict[str, Any]:
```

- **Responsabilidade**: Exibir a quantidade total de registros carregados, os campos disponíveis, o exemplo do primeiro registro e verificar linhas com dados incompletos ou nulos, retornando um dicionário com as métricas apuradas.
- **Parâmetros**:
  - `dados` (`list[dict[str, str | None]]`): Lista de dicionários representando os registros brutos de vendas carregados em memória.
- **Comportamento e Saída Padrão (`stdout`)**:
  - Sempre imprime:
    ```text

    === INSPEÇÃO INICIAL DOS DADOS ===
    Total de registros carregados: <len(dados)>
    ```
  - Se `dados` não estiver vazio (`if dados:`):
    - Extrai `campos = list(dados[0].keys())`.
    - Percorre todos os registros verificando valores `None`, `""` ou compostos apenas por espaços em branco (`valor.strip() == ""`), contabilizando `registros_incompletos` (linhas com ao menos um campo ausente) e `nulos_por_campo` (total de ausências por coluna).
    - Imprime:
      ```text
      Campos disponíveis: <campos>
      Exemplo do primeiro registro: <dados[0]>
      Registros com dados incompletos ou nulos: <registros_incompletos>
      Valores nulos/vazios por campo: <nulos_por_campo>
      ```
  - Se `dados` estiver vazio (`[]`):
    - Imprime:
      ```text
      Registros com dados incompletos ou nulos: 0
      ```
- **Garantia de Imutabilidade**:
  - Não altera, não remove e não converte nenhum elemento ou chave de `dados`.
- **Retorno**:
  - `dict[str, Any]` contendo:
    - `"total_registros"` (`int`)
    - `"campos"` (`list[str]`)
    - `"primeiro_registro"` (`dict[str, str | None] | None`)
    - `"registros_incompletos"` (`int`)
    - `"nulos_por_campo"` (`dict[str, int]`)

---

## 2. Contrato de Orquestração (`main.py`)

Dentro do bloco `if __name__ == "__main__":`, logo após `dados_brutos = mv.carregar_csv(arquivo_dados)`:

```python
mv.inspecionar_dados(dados_brutos)
```
