from app.models import Profile
from app.repositories.price_history_repository import PriceHistoryRepository


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


def test_metrics_sem_autenticacao_retorna_401(client, db_session):
    response = client.get("/admin/metrics")
    assert response.status_code == 401


def test_metrics_usuario_comum_retorna_403(client, db_session, make_auth_headers):
    _, headers = make_auth_headers()

    response = client.get("/admin/metrics", headers=headers)

    assert response.status_code == 403


def test_metrics_admin_ve_contagens_agregadas(client, db_session, make_auth_headers):
    origin, destination = _seed_airports(db_session)

    # usuário comum cria um radar
    user_id, user_headers = make_auth_headers()
    create_response = client.post("/radars", json=_radar_payload(origin, destination), headers=user_headers)
    assert create_response.status_code == 201

    # `radars` não cria profile — só /auth/me (ou o próprio /admin/metrics,
    # via require_admin) faz isso. Chama /auth/me só pra garantir a linha
    # antes de promover, do jeito mais explícito possível no teste.
    assert client.get("/auth/me", headers=user_headers).status_code == 200

    profile = db_session.get(Profile, user_id)
    profile.role = "admin"
    db_session.commit()

    response = client.get("/admin/metrics", headers=user_headers)

    assert response.status_code == 200
    body = response.json()
    assert body["total_users"] == 1
    assert body["total_radars"] == 1
    assert body["active_radars"] == 1
    assert body["new_users_7d"] == 1
    assert body["new_radars_7d"] == 1
