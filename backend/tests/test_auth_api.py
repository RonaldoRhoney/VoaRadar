import uuid

import pytest
import respx
from httpx import Response

from app.core.config import get_settings
from app.models import Profile


@pytest.fixture(autouse=True)
def _fake_supabase_url(monkeypatch):
    """`get_settings()` é `lru_cache`d — sem isso o `SUPABASE_URL` viria
    vazio do `.env` real e o `httpx.post` recusaria uma URL relativa. O
    valor é falso de propósito: respx intercepta tudo, nada sai pra rede."""
    monkeypatch.setenv("SUPABASE_URL", "https://test.supabase.co")
    monkeypatch.setenv("SUPABASE_ANON_KEY", "anon-key-fake")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@respx.mock
def test_signup_cria_sessao_e_profile(client, db_session):
    settings = get_settings()
    user_id = str(uuid.uuid4())
    respx.post(f"{settings.supabase_url}/auth/v1/signup").mock(
        return_value=Response(
            200,
            json={
                "access_token": "token-fake",
                "refresh_token": "refresh-fake",
                "expires_in": 3600,
                "user": {"id": user_id},
            },
        )
    )

    response = client.post("/auth/signup", json={"email": "user@example.com", "password": "senha-forte-123"})

    assert response.status_code == 200
    assert response.json()["access_token"] == "token-fake"
    assert db_session.get(Profile, uuid.UUID(user_id)) is not None


@respx.mock
def test_signup_com_confirmacao_pendente_nao_devolve_token(client, db_session):
    settings = get_settings()
    user_id = str(uuid.uuid4())
    respx.post(f"{settings.supabase_url}/auth/v1/signup").mock(
        return_value=Response(200, json={"user": {"id": user_id}})
    )

    response = client.post("/auth/signup", json={"email": "user@example.com", "password": "senha-forte-123"})

    assert response.status_code == 200
    assert response.json()["status"] == "confirmation_required"
    assert db_session.get(Profile, uuid.UUID(user_id)) is not None


@respx.mock
def test_signup_com_erro_do_supabase_e_400_amigavel(client, db_session):
    settings = get_settings()
    respx.post(f"{settings.supabase_url}/auth/v1/signup").mock(
        return_value=Response(422, json={"msg": "User already registered"})
    )

    response = client.post("/auth/signup", json={"email": "user@example.com", "password": "123"})

    assert response.status_code == 400
    assert "Internal Server Error" not in response.json()["detail"]
    assert "Traceback" not in response.json()["detail"]


@respx.mock
def test_login_com_credenciais_validas(client, db_session):
    settings = get_settings()
    respx.post(f"{settings.supabase_url}/auth/v1/token", params={"grant_type": "password"}).mock(
        return_value=Response(
            200, json={"access_token": "token-fake", "refresh_token": "refresh-fake", "expires_in": 3600}
        )
    )

    response = client.post("/auth/login", json={"email": "user@example.com", "password": "senha-forte-123"})

    assert response.status_code == 200
    assert response.json()["access_token"] == "token-fake"


@respx.mock
def test_login_com_credenciais_invalidas_e_401_amigavel(client, db_session):
    settings = get_settings()
    respx.post(f"{settings.supabase_url}/auth/v1/token", params={"grant_type": "password"}).mock(
        return_value=Response(400, json={"error": "invalid_grant"})
    )

    response = client.post("/auth/login", json={"email": "user@example.com", "password": "errada"})

    assert response.status_code == 401
    assert "invalid_grant" not in response.json()["detail"]


@respx.mock
def test_logout_e_sempre_204(client, db_session):
    settings = get_settings()
    respx.post(f"{settings.supabase_url}/auth/v1/logout").mock(return_value=Response(204))

    response = client.post("/auth/logout", headers={"Authorization": "Bearer token-fake"})

    assert response.status_code == 204


def test_logout_sem_token_tambem_e_204(client, db_session):
    response = client.post("/auth/logout")

    assert response.status_code == 204


def test_me_sem_autenticacao_e_401(client, db_session):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_me_usuario_comum_tem_role_user(client, db_session, make_auth_headers):
    user_id, headers = make_auth_headers(email="alguem@example.com")

    response = client.get("/auth/me", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == str(user_id)
    assert body["email"] == "alguem@example.com"
    assert body["role"] == "user"




def test_signup_sem_supabase_configurado_e_503_amigavel(client, db_session, monkeypatch):
    """SUPABASE_URL vazio (estado padrão sem .env preenchido) não pode
    virar um 500 cru — precisa de um erro amigável e estruturado."""
    monkeypatch.setenv("SUPABASE_URL", "")
    get_settings.cache_clear()

    response = client.post("/auth/signup", json={"email": "user@example.com", "password": "senha-forte-123"})

    assert response.status_code == 503
    assert "Internal Server Error" not in response.text
    get_settings.cache_clear()
