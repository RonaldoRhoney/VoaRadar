from datetime import date

from app.repositories.price_history_repository import PriceHistoryRepository
from app.services.price_intelligence_service import PriceIntelligenceService


def _seed_route_with_history(repo: PriceHistoryRepository, prices: list[float]):
    origin = repo.get_or_create_airport("BEL", "Val-de-Cans", "Belém", "Brasil")
    destination = repo.get_or_create_airport("REC", "Guararapes", "Recife", "Brasil")
    airline = repo.get_or_create_airline("AD", "Azul")
    route = repo.get_or_create_route(origin.id, destination.id)

    for i, price in enumerate(prices):
        repo.record_observation(
            route_id=route.id,
            airline_id=airline.id,
            departure_date=date(2026, 10, 14),
            return_date=date(2026, 10, 18),
            stops=1,
            duration_minutes=260,
            provider="mock",
            provider_offer_id=f"offer-rec-{i:03d}",
            price=price,
            currency="BRL",
        )
    return route


def test_analyze_route_combines_history_and_analytics(db_session):
    repo = PriceHistoryRepository(db_session)
    service = PriceIntelligenceService(repo)
    route = _seed_route_with_history(repo, [399, 620, 890])

    result = service.analyze_route(route.id, current_price=399)

    assert result.has_sufficient_data is True
    assert result.minimum == 399
    assert sorted(p.price for p in result.history) == [399.0, 620.0, 890.0]
    assert result.history == sorted(result.history, key=lambda p: p.observed_at)
    assert result.score == 100
    assert result.classification == "EXCELLENT"


def test_analyze_route_with_no_history_reports_insufficient_data(db_session):
    repo = PriceHistoryRepository(db_session)
    service = PriceIntelligenceService(repo)
    origin = repo.get_or_create_airport("GRU", "Guarulhos", "São Paulo", "Brasil")
    destination = repo.get_or_create_airport("LIS", "Humberto Delgado", "Lisboa", "Portugal")
    route = repo.get_or_create_route(origin.id, destination.id)

    result = service.analyze_route(route.id, current_price=3000)

    assert result.has_sufficient_data is False


def test_analyze_offer_resolves_route_via_provider_offer_id(db_session):
    repo = PriceHistoryRepository(db_session)
    service = PriceIntelligenceService(repo)
    _seed_route_with_history(repo, [399, 620, 890])

    result = service.analyze_offer("offer-rec-000", current_price=399)

    assert result is not None
    assert result.score == 100


def test_analyze_offer_returns_none_for_unknown_offer(db_session):
    repo = PriceHistoryRepository(db_session)
    service = PriceIntelligenceService(repo)

    result = service.analyze_offer("offer-que-nao-existe", current_price=500)

    assert result is None
