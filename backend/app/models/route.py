import uuid

from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedModel


class Route(TimestampedModel):
    __tablename__ = "routes"
    __table_args__ = (
        CheckConstraint("origin_airport_id != destination_airport_id", name="ck_route_distinct_airports"),
        UniqueConstraint("origin_airport_id", "destination_airport_id", name="uq_route_origin_destination"),
    )

    origin_airport_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("airports.id"), index=True
    )
    destination_airport_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("airports.id"), index=True
    )
