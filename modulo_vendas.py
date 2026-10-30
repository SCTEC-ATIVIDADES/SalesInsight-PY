"""Módulo de funções reutilizáveis do pipeline de vendas."""

import csv
from datetime import datetime
import json
import math
import os
from typing import Any

import pandas as pd

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


def limpar_dados(
    dados_brutos: list[dict[str, Any]],
    resumo_remocao: dict[str, int] | None = None,
) -> list[dict[str, Any]]:
    """Normaliza registros de venda, descartando linhas inválidas e duplicatas."""
    dados_limpos: list[dict[str, Any]] = []
    motivos_remocao = {
        "campo_ausente": 0,
        "campo_textual_invalido": 0,
        "data_venda_invalida": 0,
        "id_venda_invalido": 0,
        "quantidade_ausente": 0,
        "preco_unitario_ausente": 0,
        "quantidade_invalida": 0,
        "preco_unitario_invalido": 0,
        "registro_duplicado": 0,
    }
    registros_vistos: set[tuple[Any, ...]] = set()
    campos_esperados = [
        "id_venda",
        "data_venda",
        "cliente",
        "produto",
        "categoria",
        "regiao",
        "quantidade",
        "preco_unitario",
    ]
    campos_textuais = ["data_venda", "cliente", "produto", "categoria", "regiao"]
    datas_candidatas = [
        linha["data_venda"].strip()
        for linha in dados_brutos
        if isinstance(linha.get("data_venda"), str) and linha["data_venda"].strip()
    ]
    datas_parseadas = pd.to_datetime(
        pd.Series(datas_candidatas, dtype="string"),
        format="%Y-%m-%d",
        errors="coerce",
        exact=True,
    )
    datas_validas = {
        data.strftime("%Y-%m-%d")
        for data in datas_parseadas.dropna().tolist()
    }

    for linha in dados_brutos:
        motivo: str | None = None
        id_venda = 0
        quantidade = 0
        preco_unitario = 0.0
        for campo in campos_esperados:
            if campo not in linha:
                motivo = "campo_ausente"
                break

        if motivo is None:
            for campo in campos_textuais[1:]:
                valor = linha[campo]
                if valor is None or not isinstance(valor, str) or not valor.strip():
                    motivo = "campo_textual_invalido"
                    break

        textos: dict[str, str] = {}
        if motivo is None:
            for campo in campos_textuais:
                valor = linha[campo]
                if valor is None or not isinstance(valor, str):
                    motivo = "campo_textual_invalido"
                    break
                textos[campo] = valor.strip()

        if motivo is None and textos["data_venda"] not in datas_validas:
            try:
                data_validada = datetime.strptime(textos["data_venda"], "%Y-%m-%d")
                if data_validada.strftime("%Y-%m-%d") != textos["data_venda"]:
                    motivo = "data_venda_invalida"
            except ValueError:
                motivo = "data_venda_invalida"

        if motivo is None:
            valor_qtd = linha["quantidade"]
            if valor_qtd is None or not isinstance(valor_qtd, str) or not valor_qtd.strip():
                motivo = "quantidade_ausente"
            else:
                try:
                    quantidade = int(valor_qtd.strip())
                except ValueError:
                    motivo = "quantidade_invalida"

        if motivo is None:
            valor_preco = linha["preco_unitario"]
            if valor_preco is None or not isinstance(valor_preco, str) or not valor_preco.strip():
                motivo = "preco_unitario_ausente"
            else:
                try:
                    preco_unitario = float(valor_preco.strip())
                    if not math.isfinite(preco_unitario):
                        motivo = "preco_unitario_invalido"
                except ValueError:
                    motivo = "preco_unitario_invalido"

        if motivo is not None:
            motivos_remocao[motivo] += 1
            continue

        try:
            id_venda = int(linha["id_venda"])
        except (TypeError, ValueError):
            motivos_remocao["id_venda_invalido"] += 1
            continue

        registro_limpo = {
            "id_venda": id_venda,
            "data_venda": textos["data_venda"],
            "cliente": textos["cliente"],
            "produto": textos["produto"],
            "categoria": textos["categoria"],
            "regiao": textos["regiao"],
            "quantidade": quantidade,
            "preco_unitario": preco_unitario,
        }
        chave_registro = tuple(registro_limpo[campo] for campo in campos_esperados)
        if chave_registro in registros_vistos:
            motivos_remocao["registro_duplicado"] += 1
            continue

        registros_vistos.add(chave_registro)
        dados_limpos.append(registro_limpo)

    removidos = len(dados_brutos) - len(dados_limpos)
    print("\n=== RELATÓRIO DE LIMPEZA ===")
    print(
        f"Registros Válidos: {len(dados_limpos)} | "
        f"Registros Removidos: {removidos}"
    )
    print(f"Motivos de Remoção: {motivos_remocao}")
    if resumo_remocao is not None:
        resumo_remocao.update(motivos_remocao)
    return dados_limpos


def exportar_resultados(
    metricas: dict[str, Any], pasta_saida: str | os.PathLike[str] = "outputs"
) -> None:
    """Exporta métricas gerais para arquivos CSV e JSON."""
    os.makedirs(pasta_saida, exist_ok=True)
    caminho_json = os.path.join(pasta_saida, "estatisticas.json")
    caminho_csv = os.path.join(pasta_saida, "metricas_resumo.csv")

    with open(caminho_json, mode="w", encoding="utf-8") as arquivo_json:
        json.dump({"metricas_gerais": metricas}, arquivo_json, indent=4, ensure_ascii=False)

    with open(caminho_csv, mode="w", encoding="utf-8", newline="") as arquivo_csv:
        escritor = csv.writer(arquivo_csv, lineterminator="\n")
        escritor.writerow(["Métrica", "Valor"])
        for metrica, valor in metricas.items():
            escritor.writerow(
                [metrica, json.dumps(valor, ensure_ascii=False) if isinstance(valor, dict) else valor]
            )

