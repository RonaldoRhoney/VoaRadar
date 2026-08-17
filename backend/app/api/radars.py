import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.auth import get_current_user_id
from app.core.database import get_db
from app.models.radar import Radar
from app.repositories.price_history_repository import PriceHistoryRepository
from app.repositories.radar_repository import RadarNotFoundError, RadarRepository
from app.schemas.radar import RadarCreate, RadarOut, RadarUpdate
from app.services.radar_progress_service import RadarProgressService

router = APIRouter(prefix="/radars", tags=["radars"])

FRIENDLY_NOT_FOUND = "Radar não encontrado."
FRIENDLY_INVALID_AIRPORT = "Origem ou destino inválidos."
FRIENDLY_INVALID_CONDITION = "Condição do Radar incompleta — confira o valor ou a classificação escolhida."
FRIENDLY_SAME_AIRPORT = "Origem e destino não podem ser o mesmo aeroporto."
FRIENDLY_RETURN_BEFORE_DEPARTURE = "A data de volta não pode ser anterior à data de ida."


def _to_out(radar: Radar, progress_service: RadarProgressService) -> RadarOut:
    progress = progress_service.compute(radar)
    return RadarOut.model_validate(radar).model_copy(update={"progress": progress})


@router.post("", response_model=RadarOut, status_code=201)
def create_radar(
    payload: RadarCreate,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> RadarOut:
    repository = RadarRepository(db)
    try:
        radar = repository.create(user_id=user_id, **payload.model_dump())
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail=FRIENDLY_INVALID_AIRPORT)
    return _to_out(radar, RadarProgressService(PriceHistoryRepository(db)))


@router.get("", response_model=list[RadarOut])
def list_radars(
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> list[RadarOut]:
    progress_service = RadarProgressService(PriceHistoryRepository(db))
    radars = RadarRepository(db).list_for_user(user_id)
    return [_to_out(radar, progress_service) for radar in radars]


@router.get("/{radar_id}", response_model=RadarOut)
def get_radar(
    radar_id: uuid.UUID,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> RadarOut:
    try:
        radar = RadarRepository(db).get_owned(radar_id, user_id)
    except RadarNotFoundError:
        raise HTTPException(status_code=404, detail=FRIENDLY_NOT_FOUND)
    return _to_out(radar, RadarProgressService(PriceHistoryRepository(db)))


@router.put("/{radar_id}", response_model=RadarOut)
def update_radar(
    radar_id: uuid.UUID,
    payload: RadarUpdate,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> RadarOut:
    repository = RadarRepository(db)
    try:
        radar = repository.get_owned(radar_id, user_id)
    except RadarNotFoundError:
        raise HTTPException(status_code=404, detail=FRIENDLY_NOT_FOUND)

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(radar, field, value)

    # RadarCreate valida isso no schema (model_validator) — RadarUpdate é
    # parcial e não pode fazer a mesma checagem por campo isolado, então a
    # invariante é conferida aqui, no estado final já mesclado. Sem isso,
    # dava pra salvar um Radar com condition_type=PRICE_BELOW sem
    # condition_price — ele nunca dispararia, silenciosamente.
    if radar.condition_type == "PRICE_BELOW" and radar.condition_price is None:
        raise HTTPException(status_code=422, detail=FRIENDLY_INVALID_CONDITION)
    if radar.condition_type == "OPPORTUNITY_CLASSIFICATION" and radar.condition_classification is None:
        raise HTTPException(status_code=422, detail=FRIENDLY_INVALID_CONDITION)
    if radar.origin_airport_id == radar.destination_airport_id:
        raise HTTPException(status_code=422, detail=FRIENDLY_SAME_AIRPORT)
    if radar.departure_date and radar.return_date and radar.return_date < radar.departure_date:
        raise HTTPException(status_code=422, detail=FRIENDLY_RETURN_BEFORE_DEPARTURE)

    # Limpa o campo da condição anterior ao trocar de tipo — evita lixo de
    # dado que não é mais usado por nenhuma leitura, mas ficaria salvo.
    if radar.condition_type == "PRICE_BELOW":
        radar.condition_classification = None
    else:
        radar.condition_price = None

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail=FRIENDLY_INVALID_AIRPORT)
    return _to_out(radar, RadarProgressService(PriceHistoryRepository(db)))


@router.delete("/{radar_id}", status_code=204)
def delete_radar(
    radar_id: uuid.UUID,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> None:
    repository = RadarRepository(db)
    try:
        radar = repository.get_owned(radar_id, user_id)
    except RadarNotFoundError:
        raise HTTPException(status_code=404, detail=FRIENDLY_NOT_FOUND)
    repository.delete(radar)
    db.commit()
