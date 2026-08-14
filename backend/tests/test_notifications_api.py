import uuid
from datetime import date, datetime, timezone

from app.repositories.notification_repository import NotificationRepository
from app.repositories.price_history_repository import PriceHistoryRepository
from app.repositories.radar_repository import RadarRepository


def _seed_notification(db_session, user_id):
    price_repo = PriceHistoryRepository(db_session)
    radar_repo = RadarRepository(db_session)
    notification_repo = NotificationRepository(db_session)

    origin = price_repo.get_or_create_airport("BEL", "Val-de-Cans", "Belém", "Brasil")
    destination = price_repo.get_or_create_airport("REC", "Guararapes", "Recife", "Brasil")
    airline = price_repo.get_or_create_airline("AD", "Azul")
    route = price_repo.get_or_create_route(origin.id, destination.id)
    snapshot = price_repo.record_observation(
        route_id=route.id,
        airline_id=airline.id,
        departure_date=date(2026, 10, 14),
        return_date=date(2026, 10, 18),
        stops=1,
        duration_minutes=260,
        provider="mock",
        provider_offer_id="offer-rec-001",
        price=429,
        currency="BRL",
    )
    radar = radar_repo.create(
        user_id=user_id,
        name="Meu Radar Recife",
        origin_airport_id=origin.id,
        destination_airport_id=destination.id,
        condition_type="PRICE_BELOW",
        condition_price=500,
    )
    db_session.flush()
    event = radar_repo.record_match(
        radar=radar,
        price_snapshot_id=snapshot.id,
        price=429,
        score=100,
        classification="EXCELLENT",
        now=datetime.now(timezone.utc),
    )
    notification = notification_repo.create(
        user_id=user_id,
        radar_id=radar.id,
        radar_event_id=event.id,
        title="Nova oportunidade encontrada!",
        message="R$ 429, 31% abaixo da média histórica.",
    )
    db_session.commit()
    return notification


def test_listar_notificacoes_sem_autenticacao_e_401(client, db_session):
    response = client.get("/notifications")

    assert response.status_code == 401


def test_listar_notificacoes_do_usuario(client, db_session, make_auth_headers):
    user_id, headers = make_auth_headers()
    _seed_notification(db_session, user_id)

    response = client.get("/notifications", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["read_at"] is None


def test_marcar_como_lida(client, db_session, make_auth_headers):
    user_id, headers = make_auth_headers()
    notification = _seed_notification(db_session, user_id)

    response = client.patch(f"/notifications/{notification.id}/read", headers=headers)

    assert response.status_code == 200
    assert response.json()["read_at"] is not None


def test_marcar_notificacao_de_outro_usuario_como_lida_e_404(client, db_session, make_auth_headers):
    user_a = uuid.uuid4()
    notification = _seed_notification(db_session, user_a)
    _, headers_b = make_auth_headers()

    response = client.patch(f"/notifications/{notification.id}/read", headers=headers_b)

    assert response.status_code == 404


def test_notificacao_de_outro_usuario_nao_aparece_na_lista(client, db_session, make_auth_headers):
    user_a = uuid.uuid4()
    _seed_notification(db_session, user_a)
    _, headers_b = make_auth_headers()

    response = client.get("/notifications", headers=headers_b)

    assert response.status_code == 200
    assert response.json() == []
