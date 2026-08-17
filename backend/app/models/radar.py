import uuid
from datetime import date, datetime

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Numeric, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedModel, utcnow

ACTIVE = "ACTIVE"
PAUSED = "PAUSED"

PRICE_BELOW = "PRICE_BELOW"
OPPORTUNITY_CLASSIFICATION = "OPPORTUNITY_CLASSIFICATION"


class Radar(TimestampedModel):
    """Configuração persistente de vigilância de um usuário sobre uma rota
    (DATA_MODEL.md §3). `condition_type` decide qual dos dois campos de
    condição é usado — mutuamente exclusivos, validado na camada de schema,
    não como CHECK de banco (DEC-102: colunas, não tabela separada, porque
    a v0.4.0 só suporta uma condição por Radar)."""

    __tablename__ = "radars"
    __table_args__ = (
        CheckConstraint(f"condition_type IN ('{PRICE_BELOW}', '{OPPORTUNITY_CLASSIFICATION}')", name="ck_radar_condition_type"),
        CheckConstraint(f"status IN ('{ACTIVE}', '{PAUSED}')", name="ck_radar_status"),
        CheckConstraint("origin_airport_id != destination_airport_id", name="ck_radar_distinct_airports"),
        CheckConstraint(
            "return_date IS NULL OR departure_date IS NULL OR return_date >= departure_date",
            name="ck_radar_return_not_before_departure",
        ),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), index=True)
    name: Mapped[str] = mapped_column(String(255))
    origin_airport_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("airports.id"), index=True)
    destination_airport_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("airports.id"), index=True
    )
    status: Mapped[str] = mapped_column(String(16), default=ACTIVE)
    # Opcionais — Radar sem data continua vigiando a rota inteira, qualquer
    # época (comportamento anterior, preservado). Quando preenchidas, o
    # motor de avaliação só considera observação dentro da janela.
    departure_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    return_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    condition_type: Mapped[str] = mapped_column(String(32))
    condition_price: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    condition_classification: Mapped[str | None] = mapped_column(String(32), nullable=True)
    last_event_price: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    last_event_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
