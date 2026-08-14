import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user_id
from app.core.database import get_db
from app.repositories.notification_repository import NotificationNotFoundError, NotificationRepository
from app.schemas.notification import NotificationOut

router = APIRouter(prefix="/notifications", tags=["notifications"])

FRIENDLY_NOT_FOUND = "Notificação não encontrada."


@router.get("", response_model=list[NotificationOut])
def list_notifications(
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> list[NotificationOut]:
    return NotificationRepository(db).list_for_user(user_id)


@router.patch("/{notification_id}/read", response_model=NotificationOut)
def mark_read(
    notification_id: uuid.UUID,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> NotificationOut:
    repository = NotificationRepository(db)
    try:
        notification = repository.mark_read(notification_id, user_id, datetime.now(timezone.utc))
    except NotificationNotFoundError:
        raise HTTPException(status_code=404, detail=FRIENDLY_NOT_FOUND)
    db.commit()
    return notification
