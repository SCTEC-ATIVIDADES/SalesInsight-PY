import csv
from datetime import datetime
from pathlib import Path
import sys
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import gerador_dados as gd
import modulo_vendas as mv


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



