from abc import ABC, abstractmethod

from app.schemas.flight import BudgetDestination


class FlightProvider(ABC):
    """Fonte de dados de voo. Cada provedor real (Amadeus, Duffel, ...) implementa esta interface."""

    @abstractmethod
    def get_budget_destinations(
        self, origin_city: str, month: str, budget: float
    ) -> list[BudgetDestination]:
        raise NotImplementedError
