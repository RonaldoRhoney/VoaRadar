# MOCK DATA — diretório de aeroportos/companhias só pra resolver os dados
# fictícios do MockFlightProvider em entidades de banco (código, nome,
# cidade, país). Um provider real (Amadeus, Duffel...) devolveria esses
# dados prontos — essa tabela é uma ponte só pro estágio mock, não faz
# parte do contrato de FlightProvider.
MOCK_AIRPORTS: dict[str, dict[str, str]] = {
    "BEL": {"name": "Val-de-Cans", "city": "Belém", "country": "Brasil"},
    "REC": {"name": "Guararapes", "city": "Recife", "country": "Brasil"},
    "FOR": {"name": "Pinto Martins", "city": "Fortaleza", "country": "Brasil"},
    "BSB": {"name": "Presidente Juscelino Kubitschek", "city": "Brasília", "country": "Brasil"},
    "SSA": {"name": "Deputado Luís Eduardo Magalhães", "city": "Salvador", "country": "Brasil"},
}

MOCK_AIRLINE_CODES: dict[str, str] = {
    "Azul": "AD",
    "Gol": "G3",
    "LATAM": "LA",
}


def resolve_airport_code(city_name: str) -> str | None:
    normalized = city_name.strip().lower()
    for code, info in MOCK_AIRPORTS.items():
        if info["city"].lower() == normalized:
            return code
    return None


def resolve_airline_code(airline_name: str) -> str:
    return MOCK_AIRLINE_CODES.get(airline_name, airline_name[:2].upper())
