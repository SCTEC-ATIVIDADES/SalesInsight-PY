"""Ponto de entrada principal para orquestração do pipeline SalesInsight PY."""

import os

import gerador_dados as gd
import modulo_vendas as mv


def executar_pipeline() -> bool:
    """Executa o fluxo de análise e exporta resultados, reportando falhas."""
    arquivo_dados = "vendas.csv"

    try:
        if not os.path.exists(arquivo_dados):
            gd.gerar_dataset_sintetico(arquivo_dados, n_registros=150)

        dados_brutos = mv.carregar_csv(arquivo_dados)
        if not dados_brutos:
            raise ValueError("O arquivo de entrada não contém registros utilizáveis.")

        print(f"[INFO] Registros brutos carregados: {len(dados_brutos)}")
        mv.inspecionar_dados(dados_brutos)
        motivos_remocao: dict[str, int] = {}
        dados_limpos = mv.limpar_dados(dados_brutos, motivos_remocao)
        if not dados_limpos:
            raise ValueError("Nenhum registro válido após a limpeza dos dados.")

        dados_com_campos_derivados = mv.criar_campos_derivados(dados_limpos)
        metricas = {
            "registros_validos": len(dados_com_campos_derivados),
            "registros_removidos": len(dados_brutos) - len(dados_limpos),
            "motivos_remocao": motivos_remocao,
            **mv.calcular_metricas(dados_com_campos_derivados),
        }
        clientes = mv.segmentar_clientes_por_gasto(dados_com_campos_derivados)
        print(f"[RESUMO] Receita total: {metricas['total_geral']}")
        print("[RESUMO] Top clientes por gasto:")
        for nome, dados_cliente in sorted(
            clientes.items(), key=lambda item: item[1]["total_gasto"], reverse=True
        )[:5]:
            print(f"{nome}: {dados_cliente['total_gasto']} ({dados_cliente['segmento']})")
        try:
            mv.exportar_resultados(metricas, clientes)
        except Exception as erro:
            print(f"[ERRO] Falha ao exportar resultados: {erro}")
            return False
        return True
    except Exception as erro:
        print(f"[ERRO] Falha ao executar pipeline: {erro}")
        return False


if __name__ == "__main__":
    raise SystemExit(0 if executar_pipeline() else 1)
