import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedModel

OPPORTUNITY_FOUND = "OPPORTUNITY_FOUND"


class Notification(TimestampedModel):
    """`user_id` é denormalizado a partir de `radars.user_id` (evita join
    extra pra listar notificações do usuário e simplifica a policy de RLS,
    DATA_MODEL.md §5)."""

    __tablename__ = "notifications"

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), index=True)
    radar_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("radars.id"))
    radar_event_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("radar_events.id"))
    type: Mapped[str] = mapped_column(String(32), default=OPPORTUNITY_FOUND)
    title: Mapped[str] = mapped_column(String(255))
    message: Mapped[str] = mapped_column(String(500))
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
