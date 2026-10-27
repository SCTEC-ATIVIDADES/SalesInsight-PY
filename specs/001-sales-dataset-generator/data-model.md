# Data Model: RF01 – Criar ou Carregar o Dataset de Vendas

**Feature**: `001-sales-dataset-generator`  
**Date**: 2026-10-26

## 1. Entidades

### 1.1. `RegistroVendaBruto` (Linha do CSV / Dicionário em Memória)

Representa cada linha do arquivo `vendas.csv` gerada por `gerar_dataset_sintetico` e carregada por `carregar_csv` via `csv.DictReader`. Na etapa de carregamento bruto (RF01), todos os valores lidos do CSV são representados como `str` no dicionário retornado.

| Campo | Tipo no CSV / Leitura Bruta | Domínio / Formato na Geração | Regras de Ruído / Inconsistência Deliberada (RF01) |
|-------|-----------------------------|------------------------------|----------------------------------------------------|
| `id_venda` | `str` (numérico sequencial `1..n`) | Inteiro sequencial iniciando em `1` até `n_registros` | Pode aparecer duplicado devido à escrita deliberada de `dados[0]` |
| `data_venda` | `str` | Data válida em `2024` no formato ISO `YYYY-MM-DD` (gerada de forma determinística via `Faker` / semente fixa) | Formato `YYYY-MM-DD` |
| `cliente` | `str` | Identificador/nome realista de cliente (gerado de forma determinística a partir de pool de 30 clientes via `Faker('pt_BR')`) | Sem nulos no RF01 |
| `produto` | `str` | Um item entre: `"Notebook"`, `"Smartphone"`, `"Tablet"`, `"Monitor"`, `"Teclado"`, `"Mouse"` | ~10% dos registros recebem espaços sobressalentes: `f"  {prod} "` |
| `categoria` | `str` | Mapeada a partir de `produto`: `"Eletrônicos"`, `"Celulares"`, `"Acessórios"` | Consistente com o catálogo de produtos |
| `regiao` | `str` | Uma região entre: `"Sudeste"`, `"Sul"`, `"Nordeste"`, `"Centro-Oeste"`, `"Norte"` | Sem nulos no RF01 |
| `quantidade` | `str` | Inteiro convertido para string no intervalo `"1"` a `"8"` | ~5% dos registros recebem string vazia `""` (valor nulo/ausente) |
| `preco_unitario` | `str` | Float arredondado em 2 casas convertido para string no intervalo `"100.0"` a `"3500.0"` | ~5% dos registros recebem string vazia `""` (valor nulo/ausente) |

---

### 1.2. `CatalogoReferenciaVendas` (Constantes de Domínio)

Mapeamento estático que governa a coerência entre produtos, categorias e regiões na geração do dataset:

- **Produtos e Categorias**:
  - `"Notebook"` → `"Eletrônicos"`
  - `"Monitor"` → `"Eletrônicos"`
  - `"Smartphone"` → `"Celulares"`
  - `"Tablet"` → `"Celulares"`
  - `"Teclado"` → `"Acessórios"`
  - `"Mouse"` → `"Acessórios"`
- **Regiões Válidas**:
  - `["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]`
- **Cabeçalho Obrigatório (`CABECALHO_VENDAS`)**:
  - `["id_venda", "data_venda", "cliente", "produto", "categoria", "regiao", "quantidade", "preco_unitario"]`

---

## 2. Relacionamentos e Fluxo de Estado dos Dados

```text
[Catálogo de Referência + Faker(pt_BR, seed) + random(seed)]
       │
       ▼  gerar_dataset_sintetico(caminho_arquivo, n_registros=100, seed=42)
[Arquivo CSV: vendas.csv] (UTF-8, cabeçalho + 1 linha duplicada + n_registros linhas)
       │
       ▼  carregar_csv(caminho_arquivo) via csv.DictReader
[list[dict[str, str]]] (Coleção de RegistroVendaBruto em memória)
       │
       ▼  Disponível para RF02 (inspecionar_dados) e RF03 (limpar_dados)
```

## 3. Regras de Validação do Modelo (Escopo RF01)

1. **Volume Mínimo Padrão**: `n_registros` padrão igual a `100` (ou superior, como `150` quando chamado pelo `main.py`), gerando `n_registros + 1` linhas de dados no arquivo físico por conta da duplicata intencional `dados[0]`.
2. **Determinismo**: Para o mesmo par `(n_registros, seed)`, a lista de linhas geradas e o arquivo `vendas.csv` resultante são estritamente idênticos.
3. **Preservação Bruta na Leitura**: `carregar_csv` não altera nem filtra valores vazios (`""`) ou espaços (`"  Notebook "`), preservando-os fielmente para que as etapas RF02 e RF03 realizem o diagnóstico e a limpeza.
4. **Resiliência de Caminho**: Se `caminho_arquivo` não existir durante `carregar_csv`, retorna `[]` e emite aviso controlado no console sem levantar exceção não tratada.
