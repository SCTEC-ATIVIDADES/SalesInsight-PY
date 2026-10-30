import csv
from datetime import datetime
import json
from pathlib import Path
import runpy
import sys
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import gerador_dados as gd
import modulo_vendas as mv


def test_criar_campos_derivados_calcula_receita_preserva_campos_e_ordem() -> None:
    dados = [
        {"id_venda": 1, "quantidade": 3, "preco_unitario": 12.345, "cliente": "Ana"},
        {"id_venda": 2, "quantidade": 2, "preco_unitario": 250, "cliente": "Bia"},
    ]
    original = [dict(registro) for registro in dados]

    resultado = mv.criar_campos_derivados(dados)

    assert [registro["receita_total"] for registro in resultado] == [37.04, 500]
    assert [registro["id_venda"] for registro in resultado] == [1, 2]
    assert [registro["cliente"] for registro in resultado] == ["Ana", "Bia"]
    assert dados == original


def test_criar_campos_derivados_classifica_com_receita_arredondada() -> None:
    dados = [
        {"quantidade": 1, "preco_unitario": 499.994},
        {"quantidade": 1, "preco_unitario": 499.999},
        {"quantidade": 1, "preco_unitario": 500},
        {"quantidade": 1, "preco_unitario": 2000},
        {"quantidade": 1, "preco_unitario": 2000.01},
        {"quantidade": 1, "preco_unitario": 499.995},
    ]

    resultado = mv.criar_campos_derivados(dados)

    assert [registro["receita_total"] for registro in resultado] == [499.99, 500, 500, 2000, 2000.01, 500]
    assert [registro["faixa_preco"] for registro in resultado] == ["Baixo", "Médio", "Médio", "Médio", "Alto", "Médio"]


def test_criar_campos_derivados_lista_vazia() -> None:
    assert mv.criar_campos_derivados([]) == []


def test_criar_campos_derivados_processa_10000_registros() -> None:
    dados = [{"quantidade": n % 8 + 1, "preco_unitario": 123.456} for n in range(10_000)]

    resultado = mv.criar_campos_derivados(dados)

    assert len(resultado) == 10_000
    assert all("receita_total" in registro and "faixa_preco" in registro for registro in resultado)
    assert all(registro["receita_total"] == round(registro["quantidade"] * 123.456, 2) for registro in resultado)
    assert all(
        registro["faixa_preco"] == ("Baixo" if registro["receita_total"] < 500 else "Médio")
        for registro in resultado
    )


def test_gerar_dataset_sintetico_cria_arquivo_e_cabecalho(tmp_path: Path) -> None:
    arquivo = tmp_path / "vendas.csv"
    caminho = gd.gerar_dataset_sintetico(arquivo, n_registros=100, seed=42)

    assert Path(caminho) == arquivo
    assert arquivo.exists()

    with open(arquivo, mode="r", encoding="utf-8", newline="") as f:
        leitor = list(csv.reader(f))

    assert leitor[0] == gd.CABECALHO_VENDAS
    assert len(leitor) == 102
    assert leitor[1] == leitor[2]


def test_gerar_dataset_sintetico_determinismo_seed(tmp_path: Path) -> None:
    arq1 = tmp_path / "vendas_1.csv"
    arq2 = tmp_path / "vendas_2.csv"

    gd.gerar_dataset_sintetico(arq1, n_registros=100, seed=42)
    gd.gerar_dataset_sintetico(arq2, n_registros=100, seed=42)

    assert arq1.read_bytes() == arq2.read_bytes()

    with pytest.raises(ValueError):
        gd.gerar_dataset_sintetico(tmp_path / "invalido.csv", n_registros=0, seed=42)


def test_gerar_dataset_sintetico_inconsistencias_deliberadas(tmp_path: Path) -> None:
    arquivo = tmp_path / "vendas.csv"
    gd.gerar_dataset_sintetico(arquivo, n_registros=150, seed=42)

    with open(arquivo, mode="r", encoding="utf-8", newline="") as f:
        linhas = list(csv.DictReader(f))

    assert len(linhas) == 151
    assert linhas[0] == linhas[1]

    qtd_vazia = 0
    preco_vazio = 0
    produto_espacos = 0

    for linha in linhas:
        dt = datetime.strptime(linha["data_venda"], "%Y-%m-%d")
        assert dt.year == 2024
        assert linha["regiao"] in gd.REGIOES

        prod_limpo = linha["produto"].strip()
        assert prod_limpo in gd.PRODUTOS
        assert linha["categoria"] == gd.CATEGORIAS[prod_limpo]

        if linha["produto"] != prod_limpo:
            produto_espacos += 1
            assert linha["produto"] == f"  {prod_limpo} "

        if linha["quantidade"] == "":
            qtd_vazia += 1
        else:
            q = int(linha["quantidade"])
            assert 1 <= q <= 8

        if linha["preco_unitario"] == "":
            preco_vazio += 1
        else:
            p = float(linha["preco_unitario"])
            assert 100.0 <= p <= 3500.0

    assert qtd_vazia >= 1
    assert preco_vazio >= 1
    assert produto_espacos >= 1


def test_carregar_csv_retorna_lista_dicionarios_preservando_brutos(
    tmp_path: Path,
) -> None:
    arquivo = tmp_path / "vendas_teste.csv"
    with open(arquivo, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(gd.CABECALHO_VENDAS)
        writer.writerow(
            [
                "1",
                "2024-05-10",
                "Cliente_1",
                "  Notebook ",
                "Eletrônicos",
                "Sudeste",
                "",
                "2500.5",
            ]
        )

    dados = mv.carregar_csv(arquivo)
    assert isinstance(dados, list)
    assert len(dados) == 1
    assert isinstance(dados[0], dict)
    assert list(dados[0].keys()) == gd.CABECALHO_VENDAS
    assert dados[0]["produto"] == "  Notebook "
    assert dados[0]["quantidade"] == ""
    assert dados[0]["categoria"] == "Eletrônicos"


def test_carregar_csv_arquivo_inexistente_retorna_lista_vazia(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    inexistente = tmp_path / "nao_existe.csv"
    dados = mv.carregar_csv(inexistente)

    assert dados == []
    capturado = capsys.readouterr()
    assert f"[ERRO] Arquivo não encontrado: {inexistente}" in capturado.out


def test_gerar_dataset_cria_diretorio_pai_automaticamente(tmp_path: Path) -> None:
    aninhado = tmp_path / "sub1" / "sub2" / "vendas_aninhadas.csv"
    assert not aninhado.parent.exists()

    caminho = gd.gerar_dataset_sintetico(aninhado, n_registros=10, seed=42)
    assert Path(caminho) == aninhado
    assert aninhado.exists()

    dados = mv.carregar_csv(aninhado)
    assert len(dados) == 11


def test_inspecionar_dados_exibe_panorama_e_estrutura_inicial(
    capsys: pytest.CaptureFixture[str],
) -> None:
    dados: list[dict[str, str | None]] = [
        {
            "id_venda": "1",
            "data_venda": "2024-01-10",
            "cliente": "Ana Silva",
            "produto": "Notebook",
            "categoria": "Eletrônicos",
            "regiao": "Sudeste",
            "quantidade": "2",
            "preco_unitario": "3200.00",
        },
        {
            "id_venda": "2",
            "data_venda": "2024-01-11",
            "cliente": "Bruno Souza",
            "produto": "Mouse",
            "categoria": "Acessórios",
            "regiao": "Sul",
            "quantidade": "1",
            "preco_unitario": "120.50",
        },
    ]

    resumo = mv.inspecionar_dados(dados)
    capturado = capsys.readouterr()

    assert "\n=== INSPEÇÃO INICIAL DOS DADOS ===" in capturado.out
    assert "Total de registros carregados: 2" in capturado.out
    assert (
        "Campos disponíveis: ['id_venda', 'data_venda', 'cliente', 'produto', 'categoria', 'regiao', 'quantidade', 'preco_unitario']"
        in capturado.out
    )
    assert f"Exemplo do primeiro registro: {dados[0]}" in capturado.out
    assert resumo["total_registros"] == 2
    assert resumo["campos"] == gd.CABECALHO_VENDAS
    assert resumo["primeiro_registro"] == dados[0]


def test_inspecionar_dados_contabiliza_linhas_incompletas_e_nulos_por_campo(
    capsys: pytest.CaptureFixture[str],
) -> None:
    dados: list[dict[str, str | None]] = [
        {
            "id_venda": "1",
            "data_venda": "2024-01-10",
            "cliente": "Ana Silva",
            "produto": "Notebook",
            "categoria": "Eletrônicos",
            "regiao": "Sudeste",
            "quantidade": "2",
            "preco_unitario": "3200.00",
        },
        {
            "id_venda": "2",
            "data_venda": "2024-01-11",
            "cliente": "Bruno Souza",
            "produto": "Mouse",
            "categoria": "Acessórios",
            "regiao": "Sul",
            "quantidade": "",
            "preco_unitario": "120.50",
        },
        {
            "id_venda": "3",
            "data_venda": "2024-01-12",
            "cliente": "   ",
            "produto": "Teclado",
            "categoria": "Acessórios",
            "regiao": "Norte",
            "quantidade": "1",
            "preco_unitario": None,
        },
    ]

    resumo = mv.inspecionar_dados(dados)
    capturado = capsys.readouterr()

    assert resumo["total_registros"] == 3
    assert resumo["registros_incompletos"] == 2
    assert 0 <= resumo["registros_incompletos"] <= resumo["total_registros"]
    assert resumo["nulos_por_campo"] == {
        "id_venda": 0,
        "data_venda": 0,
        "cliente": 1,
        "produto": 0,
        "categoria": 0,
        "regiao": 0,
        "quantidade": 1,
        "preco_unitario": 1,
    }
    for contagem in resumo["nulos_por_campo"].values():
        assert 0 <= contagem <= resumo["total_registros"]
    assert "Registros com dados incompletos ou nulos: 2" in capturado.out
    assert (
        f"Valores nulos/vazios por campo: {resumo['nulos_por_campo']}"
        in capturado.out
    )


def test_inspecionar_dados_preserva_imutabilidade_da_entrada() -> None:
    dados_com_ruido: list[dict[str, str | None]] = [
        {
            "id_venda": "1",
            "data_venda": "2024-01-10",
            "cliente": "Ana Silva",
            "produto": "  Notebook ",
            "categoria": "Eletrônicos",
            "regiao": "Sudeste",
            "quantidade": "",
            "preco_unitario": "   ",
        }
    ]
    copia_original = [dict(linha) for linha in dados_com_ruido]

    resumo_ruido = mv.inspecionar_dados(dados_com_ruido)
    assert dados_com_ruido == copia_original
    assert resumo_ruido["registros_incompletos"] == 1

    dados_completos: list[dict[str, str | None]] = [
        {
            "id_venda": "10",
            "data_venda": "2024-02-01",
            "cliente": "Carlos Lima",
            "produto": "  Monitor ",
            "categoria": "Eletrônicos",
            "regiao": "Nordeste",
            "quantidade": "1",
            "preco_unitario": "999.90",
        }
    ]
    resumo_completo = mv.inspecionar_dados(dados_completos)
    assert resumo_completo["registros_incompletos"] == 0
    assert all(v == 0 for v in resumo_completo["nulos_por_campo"].values())


def test_limpar_dados_normaliza_registros_validos_preservando_entrada(
    capsys: pytest.CaptureFixture[str],
) -> None:
    dados = [
        {
            "id_venda": " 10 ",
            "data_venda": " 2024-02-01 ",
            "cliente": " Ana Silva ",
            "produto": " Notebook ",
            "categoria": " Eletrônicos ",
            "regiao": " Sudeste ",
            "quantidade": " 2 ",
            "preco_unitario": " 1200.50 ",
        },
        {
            "id_venda": "11",
            "data_venda": "2024-02-02",
            "cliente": "Bruno Souza",
            "produto": "Mouse",
            "categoria": "Acessórios",
            "regiao": "Sul",
            "quantidade": "1",
            "preco_unitario": "100.0",
        },
    ]
    original = [dict(linha) for linha in dados]

    resultado = mv.limpar_dados(dados)
    capsys.readouterr()

    assert resultado == [
        {
            "id_venda": 10,
            "data_venda": "2024-02-01",
            "cliente": "Ana Silva",
            "produto": "Notebook",
            "categoria": "Eletrônicos",
            "regiao": "Sudeste",
            "quantidade": 2,
            "preco_unitario": 1200.5,
        },
        {
            "id_venda": 11,
            "data_venda": "2024-02-02",
            "cliente": "Bruno Souza",
            "produto": "Mouse",
            "categoria": "Acessórios",
            "regiao": "Sul",
            "quantidade": 1,
            "preco_unitario": 100.0,
        },
    ]
    assert type(resultado[0]["id_venda"]) is int
    assert type(resultado[0]["quantidade"]) is int
    assert type(resultado[0]["preco_unitario"]) is float
    assert dados == original


def test_limpar_dados_descarta_malformados_e_reporta_motivos(
    capsys: pytest.CaptureFixture[str],
) -> None:
    base = {
        "id_venda": "1",
        "data_venda": "2024-01-10",
        "cliente": "Ana Silva",
        "produto": "Notebook",
        "categoria": "Eletrônicos",
        "regiao": "Sudeste",
        "quantidade": "2",
        "preco_unitario": "20.5",
    }
    linhas = [
        dict(base),
        {**base, "quantidade": " "},
        {**base, "preco_unitario": ""},
        {**base, "quantidade": "2.5"},
        {**base, "preco_unitario": "NaN"},
        {**base, "id_venda": "inválido"},
        {**base, "cliente": None},
        {**base, "data_venda": "2024-02-30"},
        {key: value for key, value in base.items() if key != "produto"},
    ]

    resultado = mv.limpar_dados(linhas)
    relatorio = capsys.readouterr().out

    assert len(resultado) == 1
    assert "Registros Válidos: 1 | Registros Removidos: 8" in relatorio
    assert "campo_ausente" in relatorio
    assert "campo_textual_invalido" in relatorio
    assert "data_venda_invalida" in relatorio
    assert "id_venda_invalido" in relatorio
    assert "quantidade_ausente" in relatorio
    assert "preco_unitario_ausente" in relatorio
    assert "quantidade_invalida" in relatorio
    assert "preco_unitario_invalido" in relatorio
    assert "'campo_ausente': 1" in relatorio
    assert "'campo_textual_invalido': 1" in relatorio
    assert "'data_venda_invalida': 1" in relatorio
    assert "'id_venda_invalido': 1" in relatorio
    assert "'quantidade_ausente': 1" in relatorio
    assert "'preco_unitario_ausente': 1" in relatorio
    assert "'quantidade_invalida': 1" in relatorio
    assert "'preco_unitario_invalido': 1" in relatorio


def test_limpar_dados_contabiliza_uma_razao_primaria_por_linha(
    capsys: pytest.CaptureFixture[str],
) -> None:
    linha = {
        "id_venda": "1",
        "data_venda": "2024-01-10",
        "cliente": "Ana Silva",
        "produto": "Notebook",
        "categoria": "Eletrônicos",
        "regiao": "Sudeste",
        "quantidade": "",
        "preco_unitario": "",
    }

    assert mv.limpar_dados([linha]) == []
    relatorio = capsys.readouterr().out
    assert "Registros Válidos: 0 | Registros Removidos: 1" in relatorio
    assert "'quantidade_ausente': 1" in relatorio
    assert "'preco_unitario_ausente': 0" in relatorio


def test_limpar_dados_prioriza_quantidade_antes_do_identificador(
    capsys: pytest.CaptureFixture[str],
) -> None:
    linha = {
        "id_venda": "invalido",
        "data_venda": "2024-01-10",
        "cliente": "Ana Silva",
        "produto": "Notebook",
        "categoria": "Eletrônicos",
        "regiao": "Sudeste",
        "quantidade": "invalida",
        "preco_unitario": "20.5",
    }

    assert mv.limpar_dados([linha]) == []
    relatorio = capsys.readouterr().out
    assert "'id_venda_invalido': 0" in relatorio
    assert "'quantidade_invalida': 1" in relatorio


@pytest.mark.parametrize("data_venda", ["1500-01-01", "2500-12-31"])
def test_limpar_dados_aceita_datas_validas_fora_do_limite_pandas(
    data_venda: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    linha = {
        "id_venda": "1",
        "data_venda": data_venda,
        "cliente": "Ana Silva",
        "produto": "Notebook",
        "categoria": "Eletrônicos",
        "regiao": "Sudeste",
        "quantidade": "2",
        "preco_unitario": "20.5",
    }

    resultado = mv.limpar_dados([linha])
    relatorio = capsys.readouterr().out

    assert resultado[0]["data_venda"] == data_venda
    assert "Registros Válidos: 1 | Registros Removidos: 0" in relatorio


def test_limpar_dados_valida_datas_invalidas_em_lote(
    capsys: pytest.CaptureFixture[str],
) -> None:
    base = {
        "id_venda": "1",
        "data_venda": "2024-01-10",
        "cliente": "Ana Silva",
        "produto": "Notebook",
        "categoria": "Eletrônicos",
        "regiao": "Sudeste",
        "quantidade": "2",
        "preco_unitario": "20.5",
    }
    linhas = [
        dict(base),
        {**base, "data_venda": "2024-02-30"},
        {**base, "data_venda": "2024-1-10"},
    ]

    resultado = mv.limpar_dados(linhas)
    relatorio = capsys.readouterr().out

    assert len(resultado) == 1
    assert "Registros Válidos: 1 | Registros Removidos: 2" in relatorio
    assert "'data_venda_invalida': 2" in relatorio


@pytest.mark.parametrize(
    ("campo", "valor", "motivo"),
    [
        ("quantidade", None, "quantidade_ausente"),
        ("preco_unitario", None, "preco_unitario_ausente"),
        ("preco_unitario", "   ", "preco_unitario_ausente"),
        ("preco_unitario", "inf", "preco_unitario_invalido"),
        ("data_venda", "   ", "data_venda_invalida"),
        ("data_venda", "2024-1-10", "data_venda_invalida"),
        ("cliente", "   ", "campo_textual_invalido"),
    ],
)
def test_limpar_dados_classifica_campos_nulos_e_brancos(
    campo: str,
    valor: str | None,
    motivo: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    linha: dict[str, str | None] = {
        "id_venda": "1",
        "data_venda": "2024-01-10",
        "cliente": "Ana Silva",
        "produto": "Notebook",
        "categoria": "Eletrônicos",
        "regiao": "Sudeste",
        "quantidade": "2",
        "preco_unitario": "20.5",
    }
    linha[campo] = valor

    assert mv.limpar_dados([linha]) == []
    relatorio = capsys.readouterr().out
    assert f"'{motivo}': 1" in relatorio


def test_limpar_dados_classifica_campo_obrigatorio_ausente(
    capsys: pytest.CaptureFixture[str],
) -> None:
    linha = {
        "id_venda": "1",
        "data_venda": "2024-01-10",
        "cliente": "Ana Silva",
        "categoria": "Eletrônicos",
        "regiao": "Sudeste",
        "quantidade": "2",
        "preco_unitario": "20.5",
    }

    assert mv.limpar_dados([linha]) == []
    relatorio = capsys.readouterr().out
    assert "'campo_ausente': 1" in relatorio


def test_limpar_dados_lista_vazia_retorna_contadores_zero(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert mv.limpar_dados([]) == []
    relatorio = capsys.readouterr().out
    assert "Registros Válidos: 0 | Registros Removidos: 0" in relatorio
    assert all(f"'{motivo}': 0" in relatorio for motivo in (
        "campo_ausente",
        "campo_textual_invalido",
        "data_venda_invalida",
        "id_venda_invalido",
        "quantidade_ausente",
        "preco_unitario_ausente",
        "quantidade_invalida",
        "preco_unitario_invalido",
        "registro_duplicado",
    ))


def test_limpar_dados_totais_e_motivos_reconciliam(
    capsys: pytest.CaptureFixture[str],
) -> None:
    base = {
        "id_venda": "1",
        "data_venda": "2024-01-10",
        "cliente": "Ana Silva",
        "produto": "Notebook",
        "categoria": "Eletrônicos",
        "regiao": "Sudeste",
        "quantidade": "2",
        "preco_unitario": "20.5",
    }
    linhas = [dict(base), {**base, "quantidade": "x"}, {**base, "preco_unitario": ""}]

    resultado = mv.limpar_dados(linhas)
    relatorio = capsys.readouterr().out

    assert len(resultado) + 2 == len(linhas)
    assert "Registros Válidos: 1 | Registros Removidos: 2" in relatorio
    assert "'quantidade_invalida': 1" in relatorio
    assert "'preco_unitario_ausente': 1" in relatorio


def test_limpar_dados_remove_duplicatas_exatas_e_reporta_motivo(
    capsys: pytest.CaptureFixture[str],
) -> None:
    linha = {
        "id_venda": "1",
        "data_venda": "2024-01-10",
        "cliente": "Ana Silva",
        "produto": "Notebook",
        "categoria": "Eletrônicos",
        "regiao": "Sudeste",
        "quantidade": "2",
        "preco_unitario": "20.5",
    }

    dados = [dict(linha), dict(linha), {**linha, "produto": "Mouse"}]
    resultado = mv.limpar_dados(dados)
    relatorio = capsys.readouterr().out

    assert len(resultado) == 2
    assert resultado[0]["produto"] == "Notebook"
    assert resultado[1]["produto"] == "Mouse"
    assert "Registros Válidos: 2 | Registros Removidos: 1" in relatorio
    assert "'registro_duplicado': 1" in relatorio


def test_limpar_dados_deduplica_apos_normalizar_textos(
    capsys: pytest.CaptureFixture[str],
) -> None:
    base = {
        "id_venda": "1",
        "data_venda": "2024-01-10",
        "cliente": "Ana Silva",
        "produto": "Notebook",
        "categoria": "Eletrônicos",
        "regiao": "Sudeste",
        "quantidade": "2",
        "preco_unitario": "20.5",
    }
    repetido_com_espacos = {**base, "produto": " Notebook "}

    resultado = mv.limpar_dados([base, repetido_com_espacos])
    relatorio = capsys.readouterr().out

    assert len(resultado) == 1
    assert "Registros Válidos: 1 | Registros Removidos: 1" in relatorio
    assert "'registro_duplicado': 1" in relatorio


def test_limpar_dados_registros_unicos_nao_sao_duplicatas_por_id(
    capsys: pytest.CaptureFixture[str],
) -> None:
    base = {
        "id_venda": "1",
        "data_venda": "2024-01-10",
        "cliente": "Ana Silva",
        "produto": "Notebook",
        "categoria": "Eletrônicos",
        "regiao": "Sudeste",
        "quantidade": "2",
        "preco_unitario": "20.5",
    }

    resultado = mv.limpar_dados([base, {**base, "produto": "Mouse"}])
    relatorio = capsys.readouterr().out

    assert len(resultado) == 2
    assert "Registros Válidos: 2 | Registros Removidos: 0" in relatorio
    assert "'registro_duplicado': 0" in relatorio


def test_limpar_dados_expoe_motivos_estruturados_para_integracao(
    capsys: pytest.CaptureFixture[str],
) -> None:
    linha = {
        "id_venda": "1",
        "data_venda": "2024-01-10",
        "cliente": "Ana Silva",
        "produto": "Notebook",
        "categoria": "Eletrônicos",
        "regiao": "Sudeste",
        "quantidade": "2",
        "preco_unitario": "20.5",
    }
    motivos: dict[str, int] = {}

    resultado = mv.limpar_dados([dict(linha), dict(linha)], motivos)
    capsys.readouterr()

    assert len(resultado) == 1
    assert motivos["registro_duplicado"] == 1
    assert sum(motivos.values()) == 1


def test_calcular_metricas_agrupa_receita_por_categoria_com_arredondamento() -> None:
    dados = [
        {"categoria": "A", "receita_total": 0.005},
        {"categoria": "A", "receita_total": 0.005},
        {"categoria": "B", "receita_total": 2.345},
    ]

    resultado = mv.calcular_metricas(dados)

    assert resultado["por_categoria"] == {"A": 0.01, "B": 2.35}


def test_calcular_metricas_agrupa_receita_por_regiao() -> None:
    dados = [
        {"regiao": "Norte", "receita_total": 10.125},
        {"regiao": "Norte", "receita_total": 1.125},
        {"regiao": "Sul", "receita_total": 4.50},
    ]

    resultado = mv.calcular_metricas(dados)

    assert resultado["por_regiao"] == {"Norte": 11.24, "Sul": 4.5}


def test_calcular_metricas_total_geral_vazio_e_formato() -> None:
    assert mv.calcular_metricas([]) == {
        "total_geral": 0.0,
        "por_categoria": {},
        "por_regiao": {},
    }
    assert mv.calcular_metricas([{"receita_total": 0.125}])["total_geral"] == 0.12
    assert mv.calcular_metricas(
        [{"receita_total": 1.125}, {"receita_total": 2.125}]
    )["total_geral"] == 3.25


def test_calcular_metricas_processa_10000_registros() -> None:
    dados = [
        {
            "categoria": f"C{i % 10}",
            "regiao": f"R{i % 4}",
            "receita_total": 1.0,
        }
        for i in range(10_000)
    ]

    resultado = mv.calcular_metricas(dados)

    assert resultado["total_geral"] == 10_000.0
    assert resultado["por_categoria"] == {f"C{i}": 1000.0 for i in range(10)}
    assert resultado["por_regiao"] == {f"R{i}": 2500.0 for i in range(4)}


def test_main_envia_metricas_agregadas_ao_exportador(monkeypatch: pytest.MonkeyPatch) -> None:
    dados = [{"receita_total": 10.0, "categoria": "A", "regiao": "Norte"}]
    chamadas: dict[str, object] = {}
    monkeypatch.setattr(mv, "carregar_csv", lambda _: dados)
    monkeypatch.setattr(mv, "inspecionar_dados", lambda _: {})
    monkeypatch.setattr(mv, "limpar_dados", lambda registros, _: registros)
    monkeypatch.setattr(mv, "criar_campos_derivados", lambda registros: registros)
    monkeypatch.setattr(
        mv,
        "calcular_metricas",
        lambda registros: {
            "total_geral": 10.0,
            "por_categoria": {"A": 10.0},
            "por_regiao": {"Norte": 10.0},
        },
    )
    monkeypatch.setattr(mv, "exportar_resultados", lambda metricas: chamadas.update(metricas))
    monkeypatch.setattr("os.path.exists", lambda _: True)

    runpy.run_path("main.py", run_name="__main__")

    assert chamadas["total_geral"] == 10.0
    assert chamadas["por_categoria"] == {"A": 10.0}
    assert chamadas["por_regiao"] == {"Norte": 10.0}


def test_exportar_resultados_cria_arquivos_estruturados(tmp_path: Path) -> None:
    metricas = {
        "registros_validos": 1,
        "registros_removidos": 2,
        "motivos_remocao": {"quantidade_invalida": 2, "registro_duplicado": 1},
    }

    mv.exportar_resultados(metricas, pasta_saida=tmp_path)

    caminho_csv = tmp_path / "metricas_resumo.csv"
    caminho_json = tmp_path / "estatisticas.json"
    assert caminho_csv.exists()
    assert caminho_json.exists()
    with open(caminho_csv, encoding="utf-8", newline="") as arquivo:
        assert list(csv.reader(arquivo)) == [
            ["Métrica", "Valor"],
            ["registros_validos", "1"],
            ["registros_removidos", "2"],
            ["motivos_remocao", "{\"quantidade_invalida\": 2, \"registro_duplicado\": 1}"],
        ]
    dados_json = json.loads(caminho_json.read_text(encoding="utf-8"))
    assert dados_json == {"metricas_gerais": metricas}


def test_inspecionar_dados_lista_vazia_executa_sem_erro(
    capsys: pytest.CaptureFixture[str],
) -> None:
    resumo = mv.inspecionar_dados([])
    capturado = capsys.readouterr()

    assert "\n=== INSPEÇÃO INICIAL DOS DADOS ===" in capturado.out
    assert "Total de registros carregados: 0" in capturado.out
    assert "Registros com dados incompletos ou nulos: 0" in capturado.out
    assert "Campos disponíveis:" not in capturado.out
    assert "Exemplo do primeiro registro:" not in capturado.out
    assert resumo == {
        "total_registros": 0,
        "campos": [],
        "primeiro_registro": None,
        "registros_incompletos": 0,
        "nulos_por_campo": {},
    }



