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
    motivos_remocao: dict[str, int] = {}
    dados_limpos = mv.limpar_dados(dados_brutos, motivos_remocao)
    dados_com_campos_derivados = mv.criar_campos_derivados(dados_limpos)
    metricas = {
        "registros_validos": len(dados_com_campos_derivados),
        "registros_removidos": len(dados_brutos) - len(dados_limpos),
        "motivos_remocao": motivos_remocao,
        **mv.calcular_metricas(dados_com_campos_derivados),
    }
    clientes = mv.segmentar_clientes_por_gasto(dados_com_campos_derivados)
    try:
        mv.exportar_resultados(metricas, clientes)
    except (OSError, TypeError, ValueError) as erro:
        print(f"[ERRO] Falha ao exportar resultados: {erro}")

