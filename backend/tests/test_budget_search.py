from fastapi.testclient import TestClient

from app.main import app
from app.providers.base import FlightProvider
from app.schemas.flight import BudgetDestination
from app.services.budget_search_service import BudgetSearchService

client = TestClient(app)


def _payload(budget: float = 800, origin_city: str = "Belém", month: str = "Outubro"):
    return {"budget": budget, "origin_city": origin_city, "month": month}


def test_budget_search_only_returns_destinations_within_budget():
    response = client.post("/flights/budget-search", json=_payload(budget=600))

    assert response.status_code == 200
    prices = [d["price"] for d in response.json()]
    assert prices == sorted(prices)
    assert all(price <= 600 for price in prices)


def test_budget_search_returns_empty_list_when_nothing_fits():
    response = client.post("/flights/budget-search", json=_payload(budget=1))

    assert response.status_code == 200
    assert response.json() == []


def test_budget_search_rejects_non_positive_budget():
    response = client.post("/flights/budget-search", json=_payload(budget=0))

    assert response.status_code == 422


class _FakeProvider(FlightProvider):
    def get_budget_destinations(self, origin_city, month, budget):
        return [BudgetDestination(city="Teste", uf="TS", price=100)]


def test_service_delegates_to_injected_provider():
    service = BudgetSearchService(provider=_FakeProvider())

    result = service.search(_payload_model())

    assert result == [BudgetDestination(city="Teste", uf="TS", price=100)]


def _payload_model():
    from app.schemas.flight import BudgetSearchRequest

    return BudgetSearchRequest(**_payload())
