from fastapi import APIRouter

from app.models.flight import BudgetDestination, BudgetSearchRequest

router = APIRouter(prefix="/flights", tags=["flights"])

# MOCK DATA — sem integração com fonte real de dados de voo ainda.
_MOCK_BUDGET_DESTINATIONS: list[BudgetDestination] = [
    BudgetDestination(city="Recife", uf="PE", price=429),
    BudgetDestination(city="Fortaleza", uf="CE", price=517),
    BudgetDestination(city="Brasília", uf="DF", price=598),
    BudgetDestination(city="Salvador", uf="BA", price=689),
]


@router.post("/budget-search", response_model=list[BudgetDestination])
def budget_search(payload: BudgetSearchRequest):
    return [d for d in _MOCK_BUDGET_DESTINATIONS if d.price <= payload.budget]
