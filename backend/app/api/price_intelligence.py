from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.price_history_repository import PriceHistoryRepository
from app.schemas.price_intelligence import PriceIntelligence
from app.services.price_intelligence_service import PriceIntelligenceService

router = APIRouter(prefix="/flights", tags=["price-intelligence"])

FRIENDLY_NOT_FOUND = "Ainda não temos histórico de preço para esta oferta."


@router.get("/price-intelligence/{offer_id}", response_model=PriceIntelligence)
def get_price_intelligence(
    offer_id: str,
    price: float = Query(
        ...,
        gt=0,
        lt=1_000_000,
        allow_inf_nan=False,
        description="Preço atual da oferta, a ser comparado com o histórico.",
    ),
    db: Session = Depends(get_db),
):
    service = PriceIntelligenceService(PriceHistoryRepository(db))
    result = service.analyze_offer(offer_id, current_price=price)

    if result is None:
        raise HTTPException(status_code=404, detail=FRIENDLY_NOT_FOUND)

    return result
