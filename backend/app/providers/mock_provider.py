import hashlib
from calendar import monthrange
from datetime import date

from app.providers.base import FlightProvider
from app.schemas.flight import CalendarDay, Offer, RawDestination

# Preço-base por destino, usado só pra gerar o calendário de preço por dia
# (get_price_calendar) — os mesmos 4 destinos do _MOCK_DESTINATIONS acima,
# derivado do preço da oferta mais barata de cada um.
_CALENDAR_BASE_PRICE = {"REC": 429, "FOR": 517, "BSB": 598, "SSA": 689}
_DEFAULT_BASE_PRICE = 550

# Segunda=0 ... Domingo=6. Padrão real de tarifa aérea: meio de semana mais
# barato, sexta/fim de semana mais caro — não é aleatório sem sentido.
_WEEKDAY_FACTOR = {0: 0.92, 1: 0.85, 2: 0.85, 3: 0.95, 4: 1.15, 5: 1.22, 6: 1.05}

# MOCK DATA — sem integração com fonte real de dados de voo ainda.
# Preços, datas, companhias e escalas são fictícios, mas plausíveis.
_MOCK_DESTINATIONS: list[RawDestination] = [
    RawDestination(
        id="REC",
        city="Recife",
        uf="PE",
        offers=[
            Offer(id="offer-rec-001", price=429, departure_date="2026-10-14", return_date="2026-10-18", duration_minutes=260, stops=1, airline="Azul"),
            Offer(id="offer-rec-002", price=462, departure_date="2026-10-20", return_date="2026-10-23", duration_minutes=275, stops=1, airline="Gol"),
            Offer(id="offer-rec-003", price=531, departure_date="2026-10-05", return_date="2026-10-09", duration_minutes=195, stops=0, airline="LATAM"),
        ],
    ),
    RawDestination(
        id="FOR",
        city="Fortaleza",
        uf="CE",
        offers=[
            Offer(id="offer-for-001", price=517, departure_date="2026-10-11", return_date="2026-10-15", duration_minutes=310, stops=1, airline="Gol"),
            Offer(id="offer-for-002", price=549, departure_date="2026-10-22", return_date="2026-10-26", duration_minutes=225, stops=0, airline="Azul"),
        ],
    ),
    RawDestination(
        id="BSB",
        city="Brasília",
        uf="DF",
        offers=[
            Offer(id="offer-bsb-001", price=598, departure_date="2026-10-08", return_date="2026-10-12", duration_minutes=180, stops=0, airline="LATAM"),
            Offer(id="offer-bsb-002", price=634, departure_date="2026-10-17", return_date="2026-10-21", duration_minutes=210, stops=1, airline="Gol"),
        ],
    ),
    RawDestination(
        id="SSA",
        city="Salvador",
        uf="BA",
        offers=[
            Offer(id="offer-ssa-001", price=689, departure_date="2026-10-16", return_date="2026-10-20", duration_minutes=320, stops=0, airline="LATAM"),
            Offer(id="offer-ssa-002", price=712, departure_date="2026-10-03", return_date="2026-10-07", duration_minutes=340, stops=1, airline="Azul"),
        ],
    ),
]


class MockFlightProvider(FlightProvider):
    """Provider de desenvolvimento — não representa preços reais.

    origin_city/month ainda não influenciam o resultado: o mesmo conjunto de
    destinos/ofertas aparece independente da origem/mês informados. Isso muda
    quando um provider real (ex: AmadeusProvider) for implementado.
    """

    def get_destinations(self, origin_city: str, month: str) -> list[RawDestination]:
        return _MOCK_DESTINATIONS

    def get_price_calendar(self, destination_id: str, month: str) -> list[CalendarDay]:
        """Determinístico: a mesma combinação destino+mês sempre gera os
        mesmos preços (nada de `random` sem seed) — necessário pra um mock
        ser previsível em teste e estável entre chamadas do usuário."""
        base_price = _CALENDAR_BASE_PRICE.get(destination_id, _DEFAULT_BASE_PRICE)
        year, mon = (int(part) for part in month.split("-"))
        days_in_month = monthrange(year, mon)[1]

        calendar_days = []
        for day in range(1, days_in_month + 1):
            current_date = date(year, mon, day)
            weekday_factor = _WEEKDAY_FACTOR[current_date.weekday()]

            seed = f"{destination_id}-{current_date.isoformat()}"
            digest = hashlib.sha256(seed.encode()).hexdigest()
            noise = (int(digest, 16) % 101) / 100  # 0.0–1.0, estável por data

            price = base_price * weekday_factor * (0.85 + noise * 0.3)
            calendar_days.append(CalendarDay(date=current_date.isoformat(), price=round(price, 2)))

        return calendar_days
