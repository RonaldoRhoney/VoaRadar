"""Deduplicação de notificações — ALERT_RULES.md §2. Puro, mesmo princípio
do resto do radar_engine: recebe dados, devolve booleano."""

from datetime import datetime, timedelta, timezone

COOLDOWN_HOURS = 24
MIN_IMPROVEMENT_PCT = 0.05


def should_notify(
    *, last_event_price: float | None, last_event_at: datetime | None, new_price: float, now: datetime
) -> bool:
    if last_event_at is None:
        return True
    if last_event_at.tzinfo is None:
        # SQLite (testes) não preserva timezone mesmo com DateTime(timezone=True)
        # — todo datetime gravado pela app já é UTC (utcnow(), base.py), então
        # é seguro assumir UTC aqui em vez de comparar naive com aware.
        last_event_at = last_event_at.replace(tzinfo=timezone.utc)
    cooldown_expired = (now - last_event_at) > timedelta(hours=COOLDOWN_HOURS)
    meaningful_drop = last_event_price is not None and new_price < last_event_price * (1 - MIN_IMPROVEMENT_PCT)
    return cooldown_expired or meaningful_drop
