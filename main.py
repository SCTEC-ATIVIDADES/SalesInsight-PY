"""Ponto de entrada principal para orquestração do pipeline SalesInsight PY."""

import os

from gerador_dados import gerar_dataset_sintetico
import modulo_vendas as mv


if __name__ == "__main__":
    arquivo_dados = "vendas.csv"

    if not os.path.exists(arquivo_dados):
        gerar_dataset_sintetico(arquivo_dados, n_registros=150)

    dados_brutos = mv.carregar_csv(arquivo_dados)
    print(f"[INFO] Registros brutos carregados: {len(dados_brutos)}")
    mv.inspecionar_dados(dados_brutos)

