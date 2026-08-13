import pytest

from app.collectors.flight_collector import FlightCollector, UnknownAirportError
from app.models import FlightObservation
from app.providers.mock_provider import MockFlightProvider
from app.repositories.price_history_repository import PriceHistoryRepository


def test_collect_records_a_snapshot_per_offer(db_session):
    repo = PriceHistoryRepository(db_session)
    collector = FlightCollector(MockFlightProvider(), repo)

    total_offers = sum(len(d.offers) for d in MockFlightProvider().get_destinations("Belém", "Outubro"))
    recorded = collector.collect("Belém", "Outubro")

    assert recorded == total_offers


def test_collect_is_idempotent_for_the_same_snapshot_data(db_session):
    repo = PriceHistoryRepository(db_session)
    collector = FlightCollector(MockFlightProvider(), repo)

    collector.collect("Belém", "Outubro")
    collector.collect("Belém", "Outubro")

    # Mesmos itinerários -> mesma FlightObservation, não duplica; cada
    # chamada ainda soma um PriceSnapshot novo (histórico de verdade).
    total_offers = sum(len(d.offers) for d in MockFlightProvider().get_destinations("Belém", "Outubro"))
    assert db_session.query(FlightObservation).count() == total_offers


def test_collect_raises_for_unknown_origin(db_session):
    repo = PriceHistoryRepository(db_session)
    collector = FlightCollector(MockFlightProvider(), repo)

    with pytest.raises(UnknownAirportError):
        collector.collect("Cidade Inexistente", "Outubro")


def test_collect_builds_price_history_per_route(db_session):
    repo = PriceHistoryRepository(db_session)
    collector = FlightCollector(MockFlightProvider(), repo)

    collector.collect("Belém", "Outubro")

    origin = repo.get_or_create_airport("BEL", "Val-de-Cans", "Belém", "Brasil")
    destination = repo.get_or_create_airport("REC", "Guararapes", "Recife", "Brasil")
    route = repo.get_or_create_route(origin.id, destination.id)

    history = repo.get_price_history(route.id)
    assert sorted(history) == [429.0, 462.0, 531.0]
