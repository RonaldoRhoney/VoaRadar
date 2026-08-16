import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, Integer, Numeric, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedModel, utcnow


class AnacFareReference(TimestampedModel):
    """Tarifa média mensal por rota, importada dos dados abertos da ANAC
    (PROVIDER_ARCHITECTURE.md §4). NUNCA uma oferta comprável — só
    referência estatística histórica, importada offline (nunca em
    runtime), populada por scripts/import_anac_fares.py.

    Não confundir com FlightObservation/PriceSnapshot (histórico de oferta
    real, coletado pelo FlightCollector) — são fontes e propósitos
    diferentes, mantidas em tabelas separadas de propósito.
    """

    __tablename__ = "anac_fare_reference"

    route_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("routes.id"), index=True)
    reference_month: Mapped[str] = mapped_column(String(7))  # "YYYY-MM"
    average_fare: Mapped[float] = mapped_column(Numeric(10, 2))
    sample_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source_url: Mapped[str] = mapped_column(String(500))
    imported_at: Mapped[datetime] = mapped_column(default=utcnow)
