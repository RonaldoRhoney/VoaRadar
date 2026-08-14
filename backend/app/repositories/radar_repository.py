import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Radar, RadarEvent
from app.models.radar import ACTIVE


class RadarNotFoundError(Exception):
    """Levantada tanto quando o Radar não existe quanto quando pertence a
    outro usuário — quem chama nunca distingue os dois casos (SECURITY.md
    §4: sempre 404, nunca 403, pra não vazar existência de recurso alheio)."""


class RadarRepository:
    def __init__(self, session: Session):
        self._session = session

    def create(self, **kwargs) -> Radar:
        radar = Radar(**kwargs)
        self._session.add(radar)
        self._session.flush()
        return radar

    def get_owned(self, radar_id: uuid.UUID, user_id: uuid.UUID) -> Radar:
        radar = (
            self._session.query(Radar).filter_by(id=radar_id, user_id=user_id).one_or_none()
        )
        if radar is None:
            raise RadarNotFoundError()
        return radar

    def list_for_user(self, user_id: uuid.UUID) -> list[Radar]:
        return self._session.query(Radar).filter_by(user_id=user_id).order_by(Radar.created_at.desc()).all()

    def delete(self, radar: Radar) -> None:
        self._session.delete(radar)
        self._session.flush()

    def find_active_for_route(self, origin_airport_id: uuid.UUID, destination_airport_id: uuid.UUID) -> list[Radar]:
        return (
            self._session.query(Radar)
            .filter_by(origin_airport_id=origin_airport_id, destination_airport_id=destination_airport_id, status=ACTIVE)
            .all()
        )

    def record_match(
        self,
        *,
        radar: Radar,
        price_snapshot_id: uuid.UUID,
        price: float,
        score: int | None,
        classification: str | None,
        now: datetime,
    ) -> RadarEvent:
        """Grava o evento (sempre) e atualiza o cursor de cooldown do Radar
        (last_event_price/last_event_at) — mesmo quando a notificação não
        chega a ser criada (ALERT_RULES.md §2: o log de match é completo,
        o cooldown filtra só a notificação)."""
        event = RadarEvent(
            radar_id=radar.id,
            price_snapshot_id=price_snapshot_id,
            price=price,
            score=score,
            classification=classification,
        )
        self._session.add(event)
        radar.last_event_price = price
        radar.last_event_at = now
        self._session.flush()
        return event
