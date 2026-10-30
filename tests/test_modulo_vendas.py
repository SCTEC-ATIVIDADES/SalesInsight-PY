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


