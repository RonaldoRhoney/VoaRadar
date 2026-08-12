from app.providers.base import FlightProvider
from app.schemas.flight import BudgetDestination

# MOCK DATA — sem integração com fonte real de dados de voo ainda.
_MOCK_BUDGET_DESTINATIONS: list[BudgetDestination] = [
    BudgetDestination(city="Recife", uf="PE", price=429),
    BudgetDestination(city="Fortaleza", uf="CE", price=517),
    BudgetDestination(city="Brasília", uf="DF", price=598),
    BudgetDestination(city="Salvador", uf="BA", price=689),
]


class MockFlightProvider(FlightProvider):
    """Provider de desenvolvimento — não representa preços reais.

    origin_city/month ainda não influenciam o resultado: o mock é o mesmo
    conjunto de destinos independente da origem/mês informados. Isso muda
    quando um provider real (ex: AmadeusProvider) for implementado.
    """

    def get_budget_destinations(
        self, origin_city: str, month: str, budget: float
    ) -> list[BudgetDestination]:
        return [d for d in _MOCK_BUDGET_DESTINATIONS if d.price <= budget]
