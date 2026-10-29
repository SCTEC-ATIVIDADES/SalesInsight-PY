"""Módulo de funções reutilizáveis do pipeline de vendas."""

import csv
import os
from typing import Any

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


def inspecionar_dados(
    dados: list[dict[str, str]] | list[dict[str, str | None]],
) -> dict[str, Any]:
    """Exibe o panorama inicial dos dados carregados e contabiliza registros com campos nulos ou vazios."""
    total_registros = len(dados)
    print("\n=== INSPEÇÃO INICIAL DOS DADOS ===")
    print(f"Total de registros carregados: {total_registros}")

    if not dados:
        print("Registros com dados incompletos ou nulos: 0")
        return {
            "total_registros": 0,
            "campos": [],
            "primeiro_registro": None,
            "registros_incompletos": 0,
            "nulos_por_campo": {},
        }

    campos = list(dados[0].keys())
    primeiro_registro = dados[0]
    print(f"Campos disponíveis: {campos}")
    print(f"Exemplo do primeiro registro: {primeiro_registro}")

    nulos_por_campo: dict[str, int] = {campo: 0 for campo in campos}
    registros_incompletos = 0

    for registro in dados:
        linha_incompleta = False
        for campo in campos:
            valor = registro.get(campo)
            if valor is None or (isinstance(valor, str) and valor.strip() == ""):
                nulos_por_campo[campo] += 1
                linha_incompleta = True
        if linha_incompleta:
            registros_incompletos += 1

    print(f"Registros com dados incompletos ou nulos: {registros_incompletos}")
    print(f"Valores nulos/vazios por campo: {nulos_por_campo}")

    return {
        "total_registros": total_registros,
        "campos": campos,
        "primeiro_registro": primeiro_registro,
        "registros_incompletos": registros_incompletos,
        "nulos_por_campo": nulos_por_campo,
    }

