from datetime import date

from app.collectors.airport_directory import (
    MOCK_AIRPORTS,
    resolve_airline_code,
    resolve_airport_code,
)
from app.providers.base import FlightProvider
from app.repositories.price_history_repository import PriceHistoryRepository

DEFAULT_CURRENCY = "BRL"


class UnknownAirportError(ValueError):
    pass


class FlightCollector:
    """Recebe ofertas de um FlightProvider e grava observações no histórico.

    Não analisa nada (isso é trabalho do Analytics Engine) — só normaliza e
    persiste. Hoje só sabe resolver os aeroportos do MOCK_AIRPORTS; um
    provider real viria com o próprio código IATA, sem precisar dessa ponte.
    """

    def __init__(self, provider: FlightProvider, repository: PriceHistoryRepository):
        self._provider = provider
        self._repository = repository

    def collect(self, origin_city: str, month: str) -> int:
        origin_code = resolve_airport_code(origin_city)
        if origin_code is None:
            raise UnknownAirportError(f"Aeroporto de origem desconhecido para '{origin_city}' (mock)")

        origin_info = MOCK_AIRPORTS[origin_code]
        origin_airport = self._repository.get_or_create_airport(
            origin_code, origin_info["name"], origin_info["city"], origin_info["country"]
        )

        snapshots_recorded = 0
        for raw_destination in self._provider.get_destinations(origin_city, month):
            destination_info = MOCK_AIRPORTS.get(raw_destination.id)
            destination_airport = self._repository.get_or_create_airport(
                raw_destination.id,
                destination_info["name"] if destination_info else raw_destination.city,
                raw_destination.city,
                destination_info["country"] if destination_info else "Brasil",
            )
            route = self._repository.get_or_create_route(origin_airport.id, destination_airport.id)

            for offer in raw_destination.offers:
                airline = self._repository.get_or_create_airline(
                    resolve_airline_code(offer.airline), offer.airline
                )
                self._repository.record_observation(
                    route_id=route.id,
                    airline_id=airline.id,
                    departure_date=date.fromisoformat(offer.departure_date),
                    return_date=date.fromisoformat(offer.return_date) if offer.return_date else None,
                    stops=offer.stops,
                    duration_minutes=offer.duration_minutes,
                    provider="mock",
                    provider_offer_id=offer.id,
                    price=offer.price,
                    currency=DEFAULT_CURRENCY,
                )
                snapshots_recorded += 1

        return snapshots_recorded
