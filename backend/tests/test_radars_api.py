import uuid

from app.repositories.notification_repository import NotificationRepository
from app.repositories.price_history_repository import PriceHistoryRepository
from app.repositories.radar_repository import RadarRepository


def _seed_airports(db_session):
    repo = PriceHistoryRepository(db_session)
    origin = repo.get_or_create_airport("BEL", "Val-de-Cans", "Belém", "Brasil")
    destination = repo.get_or_create_airport("REC", "Guararapes", "Recife", "Brasil")
    db_session.commit()
    return origin, destination


def _radar_payload(origin, destination):
    return {
        "name": "Meu Radar Recife",
        "origin_airport_id": str(origin.id),
        "destination_airport_id": str(destination.id),
        "condition_type": "PRICE_BELOW",
        "condition_price": 500,
    }


def test_criar_radar_sem_autenticacao_retorna_401(client, db_session):
    origin, destination = _seed_airports(db_session)

    response = client.post("/radars", json=_radar_payload(origin, destination))

    assert response.status_code == 401


def test_criar_e_listar_radar(client, db_session, make_auth_headers):
    origin, destination = _seed_airports(db_session)
    _, headers = make_auth_headers()

    create_response = client.post("/radars", json=_radar_payload(origin, destination), headers=headers)
    assert create_response.status_code == 201
    assert create_response.json()["status"] == "ACTIVE"

    list_response = client.get("/radars", headers=headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1


def test_condition_price_ausente_em_price_below_e_422(client, db_session, make_auth_headers):
    origin, destination = _seed_airports(db_session)
    _, headers = make_auth_headers()

    payload = _radar_payload(origin, destination)
    payload.pop("condition_price")

    response = client.post("/radars", json=payload, headers=headers)

    assert response.status_code == 422


def test_excluir_radar_com_eventos_e_notificacoes_nao_quebra(client, db_session, make_auth_headers):
    """Achado real (2026-08-14, testado ao vivo contra o Supabase): sem
    ON DELETE CASCADE, apagar um Radar que já disparou pelo menos uma vez
    quebrava com IntegrityError — 500 cru. Migration 0009 corrigiu."""
    from datetime import date, datetime, timezone

    price_repo = PriceHistoryRepository(db_session)
    origin, destination = _seed_airports(db_session)
    user_id, headers = make_auth_headers()

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

    radar = RadarRepository(db_session).create(
        user_id=user_id,
        name="Radar com histórico",
        origin_airport_id=origin.id,
        destination_airport_id=destination.id,
        condition_type="PRICE_BELOW",
        condition_price=500,
    )
    db_session.commit()

    event = RadarRepository(db_session).record_match(
        radar=radar,
        price_snapshot_id=snapshot.id,
        price=429,
        score=100,
        classification="EXCELLENT",
        now=datetime.now(timezone.utc),
    )
    NotificationRepository(db_session).create(
        user_id=user_id,
        radar_id=radar.id,
        radar_event_id=event.id,
        title="Nova oportunidade encontrada!",
        message="R$ 429",
    )
    db_session.commit()

    response = client.delete(f"/radars/{radar.id}", headers=headers)

    assert response.status_code == 204


class TestIDOR:
    """Matriz de teste obrigatória antes do release da v0.4.0 (SECURITY.md
    §4) — usuário B nunca pode ver, alterar ou apagar Radar do usuário A.
    Sempre 404, nunca 403 (não vaza existência do recurso)."""

    def _create_radar_for_user_a(self, client, db_session, make_auth_headers):
        origin, destination = _seed_airports(db_session)
        _, headers_a = make_auth_headers()
        response = client.post("/radars", json=_radar_payload(origin, destination), headers=headers_a)
        return response.json()["id"], headers_a

    def test_get_radar_de_outro_usuario_e_404(self, client, db_session, make_auth_headers):
        radar_id, _ = self._create_radar_for_user_a(client, db_session, make_auth_headers)
        _, headers_b = make_auth_headers()

        response = client.get(f"/radars/{radar_id}", headers=headers_b)

        assert response.status_code == 404

    def test_put_radar_de_outro_usuario_e_404(self, client, db_session, make_auth_headers):
        radar_id, _ = self._create_radar_for_user_a(client, db_session, make_auth_headers)
        _, headers_b = make_auth_headers()

        response = client.put(f"/radars/{radar_id}", json={"name": "Sequestrado"}, headers=headers_b)

        assert response.status_code == 404

    def test_delete_radar_de_outro_usuario_e_404(self, client, db_session, make_auth_headers):
        radar_id, _ = self._create_radar_for_user_a(client, db_session, make_auth_headers)
        _, headers_b = make_auth_headers()

        response = client.delete(f"/radars/{radar_id}", headers=headers_b)

        assert response.status_code == 404

    def test_dono_continua_acessando_normalmente(self, client, db_session, make_auth_headers):
        radar_id, headers_a = self._create_radar_for_user_a(client, db_session, make_auth_headers)

        response = client.get(f"/radars/{radar_id}", headers=headers_a)

        assert response.status_code == 200

    def test_lista_de_radares_nunca_inclui_radar_de_outro_usuario(self, client, db_session, make_auth_headers):
        self._create_radar_for_user_a(client, db_session, make_auth_headers)
        _, headers_b = make_auth_headers()

        response = client.get("/radars", headers=headers_b)

        assert response.status_code == 200
        assert response.json() == []
