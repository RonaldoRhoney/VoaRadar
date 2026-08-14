import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.auth import get_current_user_id
from app.core.database import get_db
from app.repositories.radar_repository import RadarNotFoundError, RadarRepository
from app.schemas.radar import RadarCreate, RadarOut, RadarUpdate

router = APIRouter(prefix="/radars", tags=["radars"])

FRIENDLY_NOT_FOUND = "Radar não encontrado."
FRIENDLY_INVALID_AIRPORT = "Origem ou destino inválidos."


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
    return radar


@router.get("", response_model=list[RadarOut])
def list_radars(
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> list[RadarOut]:
    return RadarRepository(db).list_for_user(user_id)


@router.get("/{radar_id}", response_model=RadarOut)
def get_radar(
    radar_id: uuid.UUID,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> RadarOut:
    try:
        return RadarRepository(db).get_owned(radar_id, user_id)
    except RadarNotFoundError:
        raise HTTPException(status_code=404, detail=FRIENDLY_NOT_FOUND)


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

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail=FRIENDLY_INVALID_AIRPORT)
    return radar


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
