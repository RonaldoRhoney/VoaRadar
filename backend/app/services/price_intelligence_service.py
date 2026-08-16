import uuid

from app.analytics.engine import analyze_price
from app.providers.fare_reference import FareReferenceProvider
from app.repositories.price_history_repository import PriceHistoryRepository
from app.schemas.price_intelligence import PriceHistoryPoint, PriceIntelligence


class PriceIntelligenceService:
    """Combina Repository + Analytics Engine (ARCHITECTURE.md §5). Não faz
    SQL nem estatística por conta própria — só orquestra as duas peças.

    fare_reference_provider é opcional (DEC-117/PA.3) — quando ausente ou
    quando não há referência importada pra rota, o serviço continua
    funcionando exatamente como antes, só sem o campo anac_reference
    preenchido. Uma fonte de referência indisponível NUNCA quebra o
    Price Intelligence (skill zero-cost-api — falha de fonte externa não
    derruba o produto)."""

    def __init__(self, repository: PriceHistoryRepository, fare_reference_provider: FareReferenceProvider | None = None):
        self._repository = repository
        self._fare_reference_provider = fare_reference_provider

    def analyze_route(self, route_id: uuid.UUID, current_price: float) -> PriceIntelligence:
        history = self._repository.get_price_history(route_id)
        result = analyze_price(current_price, history)

        points = self._repository.get_price_history_points(route_id)
        history_points = [PriceHistoryPoint(price=price, observed_at=observed_at) for price, observed_at in points]

        anac_reference = None
        if self._fare_reference_provider is not None:
            anac_reference = self._fare_reference_provider.get_reference(route_id)

        return result.model_copy(update={"history": history_points, "anac_reference": anac_reference})

    def analyze_offer(self, provider_offer_id: str, current_price: float) -> PriceIntelligence | None:
        """None quando a oferta não tem histórico associado ainda (nunca
        coletada) — quem chama decide como comunicar isso (ex: 404 na API)."""
        route_id = self._repository.find_route_id_by_provider_offer_id(provider_offer_id)
        if route_id is None:
            return None
        return self.analyze_route(route_id, current_price)
