import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedModel


class PriceSnapshot(TimestampedModel):
    """Um preço observado para um FlightObservation, num momento específico.

    Nunca é sobrescrito — cada coleta que encontra o mesmo itinerário de novo
    insere um snapshot novo, formando a série histórica usada pelo Analytics
    Engine (ver docs/v0.3/PRICE_INTELLIGENCE.md).
    """

    __tablename__ = "price_snapshots"

    flight_observation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("flight_observations.id"), index=True
    )
    price: Mapped[float] = mapped_column(Numeric(10, 2), index=True)
    currency: Mapped[str] = mapped_column(String(3))
    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), index=True
    )
