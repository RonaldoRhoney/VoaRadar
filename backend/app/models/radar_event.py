import uuid

from sqlalchemy import ForeignKey, Integer, Numeric, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedModel


class RadarEvent(TimestampedModel):
    """Log append-only: toda vez que o Radar Engine detecta um match, mesmo
    quando o cooldown impede a notificação (DATA_MODEL.md §4). Nunca editado
    nem apagado — é o histórico de "quando o Radar bateu"."""

    __tablename__ = "radar_events"

    radar_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("radars.id", ondelete="CASCADE"), index=True
    )
    price_snapshot_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("price_snapshots.id"))
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    classification: Mapped[str | None] = mapped_column(String(32), nullable=True)
