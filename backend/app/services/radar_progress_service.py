import uuid

from app.analytics.engine import analyze_price
from app.models.radar import PRICE_BELOW, Radar
from app.repositories.price_history_repository import PriceHistoryRepository


class RadarProgressService:
    """Estima o quão perto um Radar está de disparar, usando só dado real já
    coletado pra rota (price_snapshots) — nunca estima ou inventa um número
    (CLAUDE.md §16, mesmo princípio já aplicado em DEC-125). None quando não
    há histórico suficiente ainda: a UI decide não mostrar barra nesse caso,
    nunca mostrar 0% (0% diria "sabemos e é ruim"; None é honesto sobre
    "ainda não sabemos").

    PRICE_BELOW: compara o alvo do Radar com o menor preço já observado na
    rota (não o preço mais recente) — responde "o quão perto a melhor
    oportunidade já vista chegou do que a pessoa quer pagar".

    OPPORTUNITY_CLASSIFICATION: reaproveita o mesmo score 0-100 que o
    Analytics Engine já calcula pro Price Intelligence (PRICE_INTELLIGENCE.md
    §6), aplicado ao preço mais recente observado — não inventa uma segunda
    escala de pontuação só pra essa barra.
    """

    def __init__(self, repository: PriceHistoryRepository):
        self._repository = repository

    def compute(self, radar: Radar) -> int | None:
        route = self._repository.find_route(radar.origin_airport_id, radar.destination_airport_id)
        if route is None:
            return None
        history = self._repository.get_price_history(route.id)
        if not history:
            return None

        if radar.condition_type == PRICE_BELOW:
            return self._price_progress(radar, history)
        return self._opportunity_progress(route.id, history)

    def _price_progress(self, radar: Radar, history: list[float]) -> int | None:
        if radar.condition_price is None:
            return None
        best_price_seen = min(history)
        if best_price_seen <= 0:
            return None
        progress = (float(radar.condition_price) / best_price_seen) * 100
        return max(0, min(100, round(progress)))

    def _opportunity_progress(self, route_id: uuid.UUID, history: list[float]) -> int | None:
        points = self._repository.get_price_history_points(route_id)
        if not points:
            return None
        latest_price = points[-1][0]
        return analyze_price(latest_price, history).score
