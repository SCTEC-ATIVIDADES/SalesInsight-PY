"""Módulo independente para geração sintética e mockada do dataset de vendas."""

import csv
from datetime import date
import os
from pathlib import Path
import random
from faker import Faker

CABECALHO_VENDAS: list[str] = [
    "id_venda",
    "data_venda",
    "cliente",
    "produto",
    "categoria",
    "regiao",
    "quantidade",
    "preco_unitario",
]

PRODUTOS: list[str] = [
    "Notebook",
    "Smartphone",
    "Tablet",
    "Monitor",
    "Teclado",
    "Mouse",
]

CATEGORIAS: dict[str, str] = {
    "Notebook": "Eletrônicos",
    "Monitor": "Eletrônicos",
    "Smartphone": "Celulares",
    "Tablet": "Celulares",
    "Teclado": "Acessórios",
    "Mouse": "Acessórios",
}

REGIOES: list[str] = [
    "Sudeste",
    "Sul",
    "Nordeste",
    "Centro-Oeste",
    "Norte",
]


def gerar_dataset_sintetico(
    caminho_arquivo: str | os.PathLike[str] = "vendas.csv",
    n_registros: int = 100,
    seed: int = 42,
) -> str:
    """Gera um arquivo CSV de vendas com dados mockados e ruídos controlados."""
    if n_registros < 1:
        raise ValueError("n_registros deve ser maior ou igual a 1.")

    rng = random.Random(seed)
    fake = Faker("pt_BR")
    fake.seed_instance(seed)

    pool_clientes = [fake.name() for _ in range(30)]
    inicio_2024 = date(2024, 1, 1)
    fim_2024 = date(2024, 12, 31)

    dados: list[list[str | int | float]] = []
    for i in range(1, n_registros + 1):
        prod = rng.choice(PRODUTOS)
        cat = CATEGORIAS[prod]
        reg = rng.choice(REGIOES)
        cli = rng.choice(pool_clientes)
        dt = fake.date_between(start_date=inicio_2024, end_date=fim_2024).strftime(
            "%Y-%m-%d"
        )

        qtd: str | int = "" if rng.random() < 0.05 else rng.randint(1, 8)
        preco: str | float = (
            "" if rng.random() < 0.05 else round(rng.uniform(100, 3500), 2)
        )
        prod_sujo = f"  {prod} " if rng.random() < 0.10 else prod

        dados.append([i, dt, cli, prod_sujo, cat, reg, qtd, preco])

    destino = Path(caminho_arquivo)
    destino.parent.mkdir(parents=True, exist_ok=True)

    with open(destino, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(CABECALHO_VENDAS)
        writer.writerow(dados[0])
        writer.writerows(dados)

    print(f"[OK] Dataset gerado em: {caminho_arquivo}")
    return str(caminho_arquivo)
