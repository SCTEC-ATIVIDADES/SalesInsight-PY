"""Módulo de funções reutilizáveis do pipeline de vendas."""

import csv
import os

from gerador_dados import (
    CABECALHO_VENDAS,
    CATEGORIAS,
    PRODUTOS,
    REGIOES,
    gerar_dataset_sintetico,
)


def carregar_csv(
    caminho_arquivo: str | os.PathLike[str] = "vendas.csv",
) -> list[dict[str, str]]:
    """Carrega registros brutos de um arquivo CSV de vendas usando csv.DictReader."""
    dados: list[dict[str, str]] = []
    try:
        with open(caminho_arquivo, mode="r", encoding="utf-8", newline="") as f:
            leitor = csv.DictReader(f)
            for linha in leitor:
                dados.append(dict(linha))
    except (FileNotFoundError, OSError):
        print(f"[ERRO] Arquivo não encontrado: {caminho_arquivo}")
        return []
    return dados
