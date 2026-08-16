import uuid

from app.providers.fare_reference import FareReferenceProvider
from app.repositories.anac_fare_repository import AnacFareRepository
from app.schemas.price_intelligence import AnacReference


class AnacFareProvider(FareReferenceProvider):
    """Lê a referência já importada em anac_fare_reference — NUNCA baixa
    ou faz parsing de CSV em runtime (o CSV da ANAC é grande e a fonte é
    mensal, não uma API; importação é sempre offline, ver
    scripts/import_anac_fares.py). cost_status: ZERO_COST (skill
    zero-cost-api) — leitura do próprio banco, nenhuma chamada externa
    em tempo de requisição.
    """

    def __init__(self, repository: AnacFareRepository):
        self._repository = repository

    def get_reference(self, route_id: uuid.UUID) -> AnacReference | None:
        record = self._repository.get_latest_reference(route_id)
        if record is None:
            return None
        return AnacReference(
            average_fare=float(record.average_fare),
            reference_month=record.reference_month,
            source_url=record.source_url,
        )
