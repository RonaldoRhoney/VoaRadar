"""Importa referência de tarifa média mensal a partir dos dados abertos da
ANAC — abastece `anac_fare_reference` (AnacFareProvider, DEC-117/118 em
docs/v0.4/DECISIONS.md). NUNCA roda em runtime da API — só offline, chamado
manualmente ou por um job agendado fora do request path
(docs/PROVIDER_ARCHITECTURE.md).

Uso:
    python -m scripts.import_anac_fares --year 2025 --month 1

Fonte: sas.anac.gov.br/sas/downloads (tema "Tarifas Transporte Aéreo
Passageiros Domésticos", código 14). NÃO é um link estático — é um
formulário ASP.NET WebForms com postback; o fluxo abaixo foi verificado ao
vivo em 2026-08-17 (não é suposição): 1) GET na página pra pegar sessão +
VIEWSTATE; 2) POST simulando o autopostback do dropdown de ano
(__EVENTTARGET); 3) POST clicando "Buscar Arquivos" (só agora a listagem
reflete o ano pedido — combinar os passos 2+3 numa única requisição NÃO
funciona, a grade fica presa no ano default); 4) POST marcando o checkbox
do mês desejado + "Baixar Marcados", que devolve um ZIP com um único CSV.

Schema real do CSV (verificado baixando um arquivo de verdade, não a
documentação da ANAC, que era menos precisa): `ANO;MES;EMPRESA;ORIGEM;
DESTINO;TARIFA;ASSENTOS`, delimitador `;`, `TARIFA` com vírgula decimal
(padrão brasileiro), uma linha por combinação rota+faixa de tarifa+mês —
não por tarifa individual vendida nem por dia. A agregação por rota
(ponderada por ASSENTOS) é feita aqui, não pela ANAC.
"""

import argparse
import csv
import io
import re
import sys
import zipfile
from collections import defaultdict

import httpx

from app.core.database import get_session_factory
from app.models import Airport
from app.repositories.anac_fare_repository import AnacFareRepository
from app.repositories.price_history_repository import PriceHistoryRepository

BASE_URL = "https://sas.anac.gov.br/sas/downloads/view/frmDownload.aspx"
THEME_DOMESTIC_FARES = "14"
SOURCE_URL = "https://www.anac.gov.br/acesso-a-informacao/dados-abertos/areas-de-atuacao/voos-e-operacoes-aereas/tarifas-aereas-domesticas"

# Só os aeroportos que o VoaRadar já conhece hoje — importar o Brasil
# inteiro não é o escopo desta etapa (docs/v0.4/PROVIDER_ARCHITECTURE.md).
# ICAO (como a ANAC identifica) -> IATA (como o app identifica), verificado
# via busca real, não memória (WebSearch, 2026-08-17).
ICAO_TO_IATA = {
    "SBBE": "BEL",
    "SBRF": "REC",
    "SBFZ": "FOR",
    "SBBR": "BSB",
    "SBSV": "SSA",
}


def _extract_hidden_field(html: str, name: str) -> str:
    match = re.search(rf'{re.escape(name)}" id="{re.escape(name)}" value="([^"]*)"', html)
    return match.group(1) if match else ""


def _download_month_zip(client: httpx.Client, year: int, month: int) -> bytes:
    """Replica o fluxo de 4 passos do formulário ASP.NET — ver docstring
    do módulo pra por que não dá pra combinar os passos num só POST."""
    page = client.get(BASE_URL)
    page.raise_for_status()
    viewstate = _extract_hidden_field(page.text, "__VIEWSTATE")
    viewstate_gen = _extract_hidden_field(page.text, "__VIEWSTATEGENERATOR")

    select_year = client.post(
        BASE_URL,
        data={
            "__EVENTTARGET": "ctl00$MainContent$listAno",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": viewstate,
            "__VIEWSTATEGENERATOR": viewstate_gen,
            "ctl00$MainContent$listTema": THEME_DOMESTIC_FARES,
            "ctl00$MainContent$listAno": str(year),
        },
    )
    select_year.raise_for_status()
    viewstate = _extract_hidden_field(select_year.text, "__VIEWSTATE")
    viewstate_gen = _extract_hidden_field(select_year.text, "__VIEWSTATEGENERATOR")

    search = client.post(
        BASE_URL,
        data={
            "__VIEWSTATE": viewstate,
            "__VIEWSTATEGENERATOR": viewstate_gen,
            "ctl00$MainContent$listTema": THEME_DOMESTIC_FARES,
            "ctl00$MainContent$listAno": str(year),
            "ctl00$MainContent$btnListaArquivos": "Buscar Arquivos",
        },
    )
    search.raise_for_status()

    target_filename = f"{year}{month:02d}.CSV"
    row_index = None
    for match in re.finditer(r'chkDownload_(\d+)"[^>]*/>\s*</td><td[^>]*>([^<]+)</td>', search.text):
        if match.group(2).strip().upper() == target_filename:
            row_index = int(match.group(1))
            break
    if row_index is None:
        raise ValueError(f"Arquivo {target_filename} não encontrado na listagem da ANAC pra {year}.")

    # Nome do campo do checkbox segue a numeração de controle do GridView
    # (ctl02 = linha 0, ctl03 = linha 1, ...) — verificado ao vivo, não
    # necessariamente óbvio a partir do id="..._chkDownload_N" do HTML.
    checkbox_field = f"ctl00$MainContent$gridArquivos$ctl{row_index + 2:02d}$chkDownload"
    viewstate = _extract_hidden_field(search.text, "__VIEWSTATE")
    viewstate_gen = _extract_hidden_field(search.text, "__VIEWSTATEGENERATOR")

    download = client.post(
        BASE_URL,
        data={
            "__VIEWSTATE": viewstate,
            "__VIEWSTATEGENERATOR": viewstate_gen,
            "ctl00$MainContent$listTema": THEME_DOMESTIC_FARES,
            "ctl00$MainContent$listAno": str(year),
            checkbox_field: "on",
            "ctl00$MainContent$btnBaixar": "Baixar Marcados",
        },
    )
    download.raise_for_status()
    if not download.content.startswith(b"PK"):
        raise ValueError("A resposta da ANAC não veio como ZIP — o formulário pode ter mudado.")
    return download.content


def _parse_csv(zip_bytes: bytes) -> list[dict]:
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as archive:
        csv_name = next(name for name in archive.namelist() if name.upper().endswith(".CSV"))
        raw_text = archive.read(csv_name).decode("latin-1")

    reader = csv.DictReader(io.StringIO(raw_text), delimiter=";")
    return list(reader)


def _aggregate_by_route(rows: list[dict]) -> dict[tuple[str, str], dict]:
    """Média ponderada por ASSENTOS — uma tarifa vendida pra 40 assentos
    pesa mais que uma vendida pra 1, senão o preço médio fica distorcido
    por tarifas promocionais/residuais de baixo volume."""
    totals: dict[tuple[str, str], dict] = defaultdict(lambda: {"weighted_sum": 0.0, "seats": 0})

    for row in rows:
        origin_iata = ICAO_TO_IATA.get(row["ORIGEM"])
        destination_iata = ICAO_TO_IATA.get(row["DESTINO"])
        if origin_iata is None or destination_iata is None or origin_iata == destination_iata:
            continue

        fare = float(row["TARIFA"].replace(",", "."))
        seats = int(row["ASSENTOS"])
        if seats <= 0 or fare <= 0:
            continue

        bucket = totals[(origin_iata, destination_iata)]
        bucket["weighted_sum"] += fare * seats
        bucket["seats"] += seats

    return totals


def import_month(year: int, month: int) -> None:
    reference_month = f"{year}-{month:02d}"

    with httpx.Client(timeout=60, follow_redirects=True) as client:
        zip_bytes = _download_month_zip(client, year, month)

    rows = _parse_csv(zip_bytes)
    print(f"{len(rows)} linhas lidas do CSV da ANAC pra {reference_month}.")

    aggregated = _aggregate_by_route(rows)
    if not aggregated:
        print("Nenhuma rota entre os aeroportos conhecidos do VoaRadar apareceu nesse mês.")
        return

    session = get_session_factory()()
    try:
        price_history_repo = PriceHistoryRepository(session)
        anac_repo = AnacFareRepository(session)
        imported = 0

        for (origin_iata, destination_iata), bucket in aggregated.items():
            origin_airport = session.query(Airport).filter_by(code=origin_iata).one_or_none()
            destination_airport = session.query(Airport).filter_by(code=destination_iata).one_or_none()
            if origin_airport is None or destination_airport is None:
                # Não deveria acontecer (ICAO_TO_IATA só lista os 5
                # aeroportos que o VoaRadar já semeia), mas nunca inventa
                # um aeroporto novo aqui — import de tarifa não é o lugar
                # de criar aeroporto (CLAUDE.md §2, não codificar por cima
                # de premissa não verificada).
                continue

            route = price_history_repo.get_or_create_route(origin_airport.id, destination_airport.id)
            average_fare = round(bucket["weighted_sum"] / bucket["seats"], 2)

            anac_repo.upsert_reference(
                route_id=route.id,
                reference_month=reference_month,
                average_fare=average_fare,
                sample_size=bucket["seats"],
                source_url=SOURCE_URL,
            )
            imported += 1
            print(f"  {origin_iata}->{destination_iata}: R$ {average_fare:.2f} (amostra: {bucket['seats']} assentos)")

        session.commit()
        print(f"{imported} rota(s) importada(s) pra {reference_month}.")
    finally:
        session.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--month", type=int, required=True, choices=range(1, 13))
    args = parser.parse_args()

    try:
        import_month(args.year, args.month)
    except Exception as error:  # noqa: BLE001 — script de linha de comando, erro cru é aceitável aqui
        print(f"Falhou: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
