from app.providers.base import FlightProvider
from app.schemas.flight import ExploreRequest, Offer, RawDestination
from app.services.explore_service import ExploreService


def _request(budget: float = 800, origin_city: str = "Belém", month: str = "Outubro"):
    return ExploreRequest(budget=budget, origin_city=origin_city, month=month)


class _FakeProvider(FlightProvider):
    def __init__(self, destinations: list[RawDestination]):
        self._destinations = destinations

    def get_destinations(self, origin_city, month):
        return self._destinations

    def get_price_calendar(self, destination_id, month):
        return []


def test_only_offers_within_budget_are_kept():
    destinations = [
        RawDestination(
            id="REC",
            city="Recife",
            uf="PE",
            offers=[
                Offer(id="o1", price=429, departure_date="2026-10-14", duration_minutes=260, stops=1, airline="Azul"),
                Offer(id="o2", price=1200, departure_date="2026-10-20", duration_minutes=260, stops=1, airline="Azul"),
            ],
        )
    ]
    service = ExploreService(provider=_FakeProvider(destinations))

    result = service.explore(_request(budget=800))

    assert len(result.destinations) == 1
    assert [o.id for o in result.destinations[0].offers] == ["o1"]
    assert result.destinations[0].best_offer.id == "o1"


def test_destinations_sorted_by_best_offer_price():
    destinations = [
        RawDestination(id="A", city="A", uf="AA", offers=[Offer(id="a1", price=700, departure_date="2026-10-01", duration_minutes=100, stops=0, airline="X")]),
        RawDestination(id="B", city="B", uf="BB", offers=[Offer(id="b1", price=400, departure_date="2026-10-01", duration_minutes=100, stops=0, airline="X")]),
    ]
    service = ExploreService(provider=_FakeProvider(destinations))

    result = service.explore(_request(budget=800))

    assert [d.id for d in result.destinations] == ["B", "A"]


def test_cheapest_destination_gets_best_price_highlight():
    destinations = [
        RawDestination(id="A", city="A", uf="AA", offers=[Offer(id="a1", price=700, departure_date="2026-10-01", duration_minutes=100, stops=0, airline="X")]),
        RawDestination(id="B", city="B", uf="BB", offers=[Offer(id="b1", price=400, departure_date="2026-10-01", duration_minutes=100, stops=0, airline="X")]),
    ]
    service = ExploreService(provider=_FakeProvider(destinations))

    result = service.explore(_request(budget=800))

    highlighted = [d for d in result.destinations if d.highlight == "best_price"]
    assert [d.id for d in highlighted] == ["B"]


def test_near_budget_returned_when_nothing_fits():
    destinations = [
        RawDestination(id="A", city="A", uf="AA", offers=[Offer(id="a1", price=537, departure_date="2026-10-01", duration_minutes=100, stops=0, airline="X")]),
    ]
    service = ExploreService(provider=_FakeProvider(destinations))

    result = service.explore(_request(budget=500))

    assert result.destinations == []
    assert [d.id for d in result.near_budget] == ["A"]
    assert result.near_budget[0].budget_status == "near_budget"


def test_metadata_reflects_results():
    destinations = [
        RawDestination(id="A", city="A", uf="AA", offers=[Offer(id="a1", price=700, departure_date="2026-10-01", duration_minutes=100, stops=0, airline="X")]),
        RawDestination(id="B", city="B", uf="BB", offers=[Offer(id="b1", price=400, departure_date="2026-10-01", duration_minutes=100, stops=0, airline="X")]),
    ]
    service = ExploreService(provider=_FakeProvider(destinations))

    result = service.explore(_request(budget=800))

    assert result.metadata.result_count == 2
    assert result.metadata.cheapest_price == 400
