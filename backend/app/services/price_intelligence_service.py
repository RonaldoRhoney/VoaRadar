import uuid

from app.analytics.engine import analyze_price
from app.repositories.price_history_repository import PriceHistoryRepository
from app.schemas.price_intelligence import PriceIntelligence


class PriceIntelligenceService:
    """Combina Repository + Analytics Engine (ARCHITECTURE.md §5). Não faz
    SQL nem estatística por conta própria — só orquestra as duas peças."""

    def __init__(self, repository: PriceHistoryRepository):
        self._repository = repository

    def analyze_route(self, route_id: uuid.UUID, current_price: float) -> PriceIntelligence:
        history = self._repository.get_price_history(route_id)
        return analyze_price(current_price, history)

    def analyze_offer(self, provider_offer_id: str, current_price: float) -> PriceIntelligence | None:
        """None quando a oferta não tem histórico associado ainda (nunca
        coletada) — quem chama decide como comunicar isso (ex: 404 na API)."""
        route_id = self._repository.find_route_id_by_provider_offer_id(provider_offer_id)
        if route_id is None:
            return None
        return self.analyze_route(route_id, current_price)
