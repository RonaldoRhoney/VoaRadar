from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Airport
from app.schemas.airport import AirportOut

router = APIRouter(prefix="/airports", tags=["airports"])


@router.get("", response_model=list[AirportOut])
def list_airports(db: Session = Depends(get_db)) -> list[AirportOut]:
    """Dado público (nome/cidade de aeroporto, sem informação sensível) —
    alimenta o seletor de origem/destino na criação de um Radar (v0.4)."""
    return db.query(Airport).order_by(Airport.city).all()
