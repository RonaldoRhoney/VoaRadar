import uuid
from datetime import date, datetime, timezone

from app.models.notification import OPPORTUNITY_FOUND
from app.models.radar import Radar
from app.radar_engine.cooldown import should_notify
from app.radar_engine.engine import RadarCondition, evaluate_radar
from app.repositories.notification_repository import NotificationRepository
from app.repositories.price_history_repository import PriceHistoryRepository
from app.repositories.radar_repository import RadarRepository
from app.services.price_intelligence_service import PriceIntelligenceService


class RadarEvaluationService:
    """Orquestra repository + Radar Engine + cooldown (ARCHITECTURE.md §5) —
    mesma divisão de responsabilidade que PriceIntelligenceService já usa
    entre repository e analytics engine."""

    def __init__(
        self,
        price_history_repository: PriceHistoryRepository,
        radar_repository: RadarRepository,
        notification_repository: NotificationRepository,
    ):
        self._price_history_repository = price_history_repository
        self._radar_repository = radar_repository
        self._notification_repository = notification_repository
        self._price_intelligence_service = PriceIntelligenceService(price_history_repository)

    def evaluate_for_route(
        self,
        *,
        route_id: uuid.UUID,
        current_price: float,
        price_snapshot_id: uuid.UUID,
        departure_date: date | None = None,
        return_date: date | None = None,
    ) -> None:
        """Chamado logo após um novo PriceSnapshot ser persistido
        (RADAR_ENGINE.md §3) — orientado a evento, não por polling.

        `departure_date`/`return_date` são os da observação que gerou este
        snapshot — usados só pra filtrar Radar com data marcada (2026-08-17:
        "campo ida e volta"). Radar sem data (comportamento anterior)
        continua vigiando a rota inteira, qualquer época."""
        route = self._price_history_repository.get_route(route_id)
        if route is None:
            return

        candidates = self._radar_repository.find_active_for_route(
            route.origin_airport_id, route.destination_airport_id
        )
        candidates = [
            radar for radar in candidates if _dates_match(radar, departure_date, return_date)
        ]
        if not candidates:
            return

        intelligence = self._price_intelligence_service.analyze_route(route_id, current_price)
        now = datetime.now(timezone.utc)

        for radar in candidates:
            condition = RadarCondition(
                condition_type=radar.condition_type,
                condition_price=float(radar.condition_price) if radar.condition_price is not None else None,
                condition_classification=radar.condition_classification,
            )
            matched = evaluate_radar(condition, current_price, intelligence.classification)
            if not matched:
                continue

            notify = should_notify(
                last_event_price=float(radar.last_event_price) if radar.last_event_price is not None else None,
                last_event_at=radar.last_event_at,
                new_price=current_price,
                now=now,
            )

            event = self._radar_repository.record_match(
                radar=radar,
                price_snapshot_id=price_snapshot_id,
                price=current_price,
                score=intelligence.score,
                classification=intelligence.classification,
                now=now,
            )

            if notify:
                self._notification_repository.create(
                    user_id=radar.user_id,
                    radar_id=radar.id,
                    radar_event_id=event.id,
                    type=OPPORTUNITY_FOUND,
                    title="Nova oportunidade encontrada!",
                    message=_build_message(radar.name, current_price, intelligence.percentage_vs_mean),
                )


def _dates_match(radar: Radar, observation_departure: date | None, observation_return: date | None) -> bool:
    """Comparação exata, deliberadamente simples pra essa primeira versão
    do filtro (data única, não uma janela de flexibilidade) — evoluir pra
    intervalo é trabalho futuro, não escopo deste pedido."""
    if radar.departure_date is not None and radar.departure_date != observation_departure:
        return False
    if radar.return_date is not None and radar.return_date != observation_return:
        return False
    return True


def _build_message(radar_name: str, price: float, percentage_vs_mean: float | None) -> str:
    base = f"{radar_name}: R$ {price:.2f}"
    if percentage_vs_mean is not None and percentage_vs_mean < 0:
        return f"{base}, {abs(percentage_vs_mean):.0f}% abaixo da média histórica."
    return f"{base} — condição do seu Radar atingida."
