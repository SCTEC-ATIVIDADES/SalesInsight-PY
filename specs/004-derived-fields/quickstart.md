# Quickstart: Validar Campos Derivados

## Pré-requisitos

- Python 3.11+ e dependências do projeto instaladas (`requirements.txt`).
- Executar a partir da raiz do repositório.

## Validação

1. Executar testes focados: `pytest tests/test_modulo_vendas.py`.
2. Confirmar cobertura de receita arredondada, limites de R$ 500 e R$ 2.000, preservação de campos/ordem e lista vazia.
3. Executar suíte completa: `pytest`.
4. Executar pipeline: `python main.py`; confirmar conclusão sem erro.
5. Validar ambiente conteinerizado: `docker compose run --rm --entrypoint pytest app` e `docker compose run --rm app` (o serviço executa `python main.py` por padrão).

## Referências

- Regras e critérios: [spec.md](./spec.md)
- Estrutura dos registros: [data-model.md](./data-model.md)
- Contrato: [contracts/derived-sales-fields-contract.md](./contracts/derived-sales-fields-contract.md)
