import re

from fastapi import APIRouter, HTTPException, Query

from app.schemas.flight import ExploreRequest, ExploreResponse, PriceCalendarResponse
from app.services.explore_service import ExploreService
from app.services.price_calendar_service import PriceCalendarService

router = APIRouter(prefix="/flights", tags=["flights"])

_MONTH_PATTERN = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
FRIENDLY_INVALID_MONTH = "Informe o mês no formato AAAA-MM (ex: 2026-10)."


@router.post("/explore", response_model=ExploreResponse)
def explore(payload: ExploreRequest):
    service = ExploreService()
    return service.explore(payload)


@router.get("/calendar", response_model=PriceCalendarResponse)
def price_calendar(
    destination_id: str = Query(..., min_length=1),
    month: str = Query(..., description="Formato AAAA-MM, ex: 2026-10"),
):
    if not _MONTH_PATTERN.match(month):
        raise HTTPException(status_code=422, detail=FRIENDLY_INVALID_MONTH)
    service = PriceCalendarService()
    return service.get_calendar(destination_id, month)
