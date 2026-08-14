import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Notification


class NotificationNotFoundError(Exception):
    """Mesma lógica de RadarNotFoundError — usada pra sempre responder 404
    (nunca 403) em acesso cross-user (SECURITY.md §4)."""


class NotificationRepository:
    def __init__(self, session: Session):
        self._session = session

    def create(self, **kwargs) -> Notification:
        notification = Notification(**kwargs)
        self._session.add(notification)
        self._session.flush()
        return notification

    def list_for_user(self, user_id: uuid.UUID) -> list[Notification]:
        return (
            self._session.query(Notification)
            .filter_by(user_id=user_id)
            .order_by(Notification.created_at.desc())
            .all()
        )

    def mark_read(self, notification_id: uuid.UUID, user_id: uuid.UUID, now: datetime) -> Notification:
        notification = (
            self._session.query(Notification).filter_by(id=notification_id, user_id=user_id).one_or_none()
        )
        if notification is None:
            raise NotificationNotFoundError()
        notification.read_at = now
        self._session.flush()
        return notification
