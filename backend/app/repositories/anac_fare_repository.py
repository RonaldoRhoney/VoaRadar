import uuid

from sqlalchemy.orm import Session

from app.models import AnacFareReference


class AnacFareRepository:
    """Único lugar que fala SQL/ORM pra anac_fare_reference (mesmo padrão
    de PriceHistoryRepository, ARCHITECTURE.md §4)."""

    def __init__(self, session: Session):
        self._session = session

    def get_latest_reference(self, route_id: uuid.UUID) -> AnacFareReference | None:
        """Referência mais recente pra rota, se houver mais de um mês
        importado — nunca faz sentido misturar meses diferentes numa
        mesma resposta."""
        return (
            self._session.query(AnacFareReference)
            .filter_by(route_id=route_id)
            .order_by(AnacFareReference.reference_month.desc())
            .first()
        )

    def upsert_reference(
        self,
        *,
        route_id: uuid.UUID,
        reference_month: str,
        average_fare: float,
        sample_size: int | None,
        source_url: str,
    ) -> AnacFareReference:
        existing = (
            self._session.query(AnacFareReference)
            .filter_by(route_id=route_id, reference_month=reference_month)
            .one_or_none()
        )
        if existing is not None:
            existing.average_fare = average_fare
            existing.sample_size = sample_size
            existing.source_url = source_url
            self._session.flush()
            return existing

        reference = AnacFareReference(
            route_id=route_id,
            reference_month=reference_month,
            average_fare=average_fare,
            sample_size=sample_size,
            source_url=source_url,
        )
        self._session.add(reference)
        self._session.flush()
        return reference
