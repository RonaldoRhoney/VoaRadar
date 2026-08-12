from app.providers.base import FlightProvider
from app.providers.mock_provider import MockFlightProvider
from app.schemas.flight import BudgetDestination, BudgetSearchRequest


class BudgetSearchService:
    def __init__(self, provider: FlightProvider | None = None):
        self._provider = provider or MockFlightProvider()

    def search(self, request: BudgetSearchRequest) -> list[BudgetDestination]:
        destinations = self._provider.get_budget_destinations(
            origin_city=request.origin_city,
            month=request.month,
            budget=request.budget,
        )
        return sorted(destinations, key=lambda d: d.price)
