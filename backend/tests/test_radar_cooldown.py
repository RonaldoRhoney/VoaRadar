from datetime import datetime, timedelta, timezone

from app.radar_engine.cooldown import should_notify

NOW = datetime(2026, 8, 13, 12, 0, tzinfo=timezone.utc)


def test_primeira_ocorrencia_sempre_notifica():
    assert should_notify(last_event_price=None, last_event_at=None, new_price=429, now=NOW) is True


def test_dentro_do_cooldown_sem_queda_significativa_nao_notifica():
    last_event_at = NOW - timedelta(hours=1)
    assert should_notify(last_event_price=429, last_event_at=last_event_at, new_price=428, now=NOW) is False


def test_cooldown_expirado_notifica_mesmo_sem_queda():
    last_event_at = NOW - timedelta(hours=25)
    assert should_notify(last_event_price=429, last_event_at=last_event_at, new_price=429, now=NOW) is True


def test_queda_significativa_notifica_mesmo_dentro_do_cooldown():
    last_event_at = NOW - timedelta(hours=1)
    # 429 * 0.95 = 407.55 — precisa cair abaixo disso
    assert should_notify(last_event_price=429, last_event_at=last_event_at, new_price=400, now=NOW) is True


def test_queda_no_limite_exato_nao_conta_como_significativa():
    last_event_at = NOW - timedelta(hours=1)
    assert should_notify(last_event_price=500, last_event_at=last_event_at, new_price=475, now=NOW) is False
