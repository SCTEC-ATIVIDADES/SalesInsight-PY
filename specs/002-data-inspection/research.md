# Phase 0 Research: RF02 – Inspecionar e Descrever os Dados

**Feature**: `002-data-inspection`
**Date**: 2026-10-28

## 1. Formato de Saída no Console e Compatibilidade com o Exemplo do RF02

- **Decision**: Manter na função `inspecionar_dados(dados)` exatamente as 4 mensagens de `print` fornecidas no exemplo de referência do RF02 quando `dados` não estiver vazio (`\n=== INSPEÇÃO INICIAL DOS DADOS ===`, `Total de registros carregados: {len(dados)}`, `Campos disponíveis: {list(dados[0].keys())}`, `Exemplo do primeiro registro: {dados[0]}`) e adicionar em seguida a exibição explícita da contagem de linhas com dados incompletos ou nulos (`Registros com dados incompletos ou nulos: {registros_incompletos}`) e dos nulos por campo (`Valores nulos/vazios por campo: {nulos_por_campo}`).
- **Rationale**:
  - Preserva 100% de fidelidade com o trecho de exemplo do enunciado do RF02.
  - Atende simultaneamente à exigência textual do requisito ("verificar linhas com dados incompletos ou nulos"), tornando o diagnóstico visível tanto no terminal ao rodar `python main.py` quanto verificável via `capsys` nos testes.
- **Alternatives considered**:
  - *Imprimir apenas as 4 linhas do exemplo sem reportar linhas incompletas/nulas*: Descumpriria metade do enunciado do RF02 ("verificar linhas com dados incompletos ou nulos") e dificultaria a auditoria de qualidade exigida pelo Princípio IV da Constituição.
  - *Alterar o texto das linhas do exemplo*: Poderia quebrar verificações visuais ou automatizadas baseadas no enunciado.

## 2. Critério de Detecção de Dados Incompletos ou Nulos

- **Decision**: Percorrer cada registro e cada campo com laços `for` explícitos, classificando um valor como incompleto/nulo quando for `None` ou quando, convertido/tratado como `str`, resultar em string vazia após remoção de espaços (`valor.strip() == ""`). Uma linha é contabilizada uma única vez em `registros_incompletos` se possuir ao menos um campo ausente/nulo, enquanto `nulos_por_campo` acumula a quantidade de ocorrências ausentes em cada coluna individualmente.
- **Rationale**:
  - Como `csv.DictReader` retorna strings vazias (`""`) para células vazias e pode retornar `None` caso uma linha tenha menos colunas que o cabeçalho, verificar `valor is None or (isinstance(valor, str) and valor.strip() == "")` cobre todos os casos reais de CSV e chamadas diretas em memória.
  - Contabilizar `registros_incompletos` por linha (usando uma flag booleana explícita `linha_incompleta`) evita dupla contagem quando um mesmo registro tem mais de um campo vazio.
- **Alternatives considered**:
  - *Somar os nulos de todas as colunas como total de linhas incompletas*: Incorreto quando uma mesma linha possui dois campos vazios (ex.: `quantidade=""` e `preco_unitario=""`), pois inflaria o número de linhas afetadas.
  - *Usar `pandas.DataFrame(dados).isna()` com expressões encadeadas opacas*: O Princípio II da Constituição prioriza laços `for` e estruturas condicionais explícitas e legíveis; além disso, strings vazias `""` vindas de `csv.DictReader` não são consideradas `NaN` por padrão no `pandas` sem conversão prévia.

## 3. Contrato de Retorno da Função `inspecionar_dados`

- **Decision**: Além de exibir o resumo no console (`stdout`), retornar um dicionário tipado (`dict[str, Any]`) contendo `total_registros`, `campos`, `primeiro_registro`, `registros_incompletos` e `nulos_por_campo`.
- **Rationale**:
  - Chamadores que usam `inspecionar_dados(dados)` apenas como procedimento (como `main.py` no exemplo) simplesmente ignoram o valor de retorno sem qualquer impacto.
  - Testes unitários em `tests/test_modulo_vendas.py` podem validar tanto a saída de console (`capsys`) quanto os valores exatos calculados na estrutura retornada, seguindo o Princípio I ("assinatura com parâmetros e retornos explícitos") e o Princípio III (TDD).
- **Alternatives considered**:
  - *Retornar `None`*: Obrigaria todos os testes a fazer parsing de strings do `stdout` para verificar contagens numéricas de linhas incompletas e nulos por coluna.
