from fastapi import APIRouter

from app.schemas.flight import BudgetDestination, BudgetSearchRequest
from app.services.budget_search_service import BudgetSearchService

router = APIRouter(prefix="/flights", tags=["flights"])


@router.post("/budget-search", response_model=list[BudgetDestination])
def budget_search(payload: BudgetSearchRequest):
    service = BudgetSearchService()
    return service.search(payload)
