import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedModel


class FlightObservation(TimestampedModel):
    """Um itinerário distinto (rota + companhia + datas + escalas + duração).

    Deduplicado pela chave natural abaixo: coletas repetidas do mesmo
    itinerário não criam uma linha nova, só um novo `PriceSnapshot` — é
    assim que o histórico de preço se forma para um mesmo voo ao longo do
    tempo, em vez de virar uma tabela de "todo evento de coleta".
    """

    __tablename__ = "flight_observations"
    __table_args__ = (
        UniqueConstraint(
            "route_id",
            "airline_id",
            "departure_date",
            "return_date",
            "stops",
            "duration_minutes",
            "provider",
            name="uq_flight_observation_itinerary",
        ),
    )

    route_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("routes.id"), index=True)
    airline_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("airlines.id"), index=True)
    departure_date: Mapped[date] = mapped_column(Date, index=True)
    return_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    stops: Mapped[int] = mapped_column(Integer)
    duration_minutes: Mapped[int] = mapped_column(Integer)
    provider: Mapped[str] = mapped_column(String(64))
    provider_offer_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
