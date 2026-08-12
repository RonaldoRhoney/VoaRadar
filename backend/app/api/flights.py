from fastapi import APIRouter

from app.schemas.flight import ExploreRequest, ExploreResponse
from app.services.explore_service import ExploreService

router = APIRouter(prefix="/flights", tags=["flights"])


@router.post("/explore", response_model=ExploreResponse)
def explore(payload: ExploreRequest):
    service = ExploreService()
    return service.explore(payload)
