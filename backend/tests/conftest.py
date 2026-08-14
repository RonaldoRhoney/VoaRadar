import uuid

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import ec
from fastapi.testclient import TestClient
from jwt.algorithms import ECAlgorithm
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401 — registra os models na metadata do Base
from app.core.auth import get_jwks
from app.core.database import Base, get_db

# Chave EC gerada uma vez por sessão de testes, só pra assinar/validar
# tokens de teste — simula o par de chaves ECC/ES256 que o Supabase Auth
# usa de verdade (confirmado em Settings > JWT Keys), sem bater na rede.
_TEST_KEY = ec.generate_private_key(ec.SECP256R1())
_TEST_KID = "test-key"
_TEST_ALG = ECAlgorithm(ECAlgorithm.SHA256)
_TEST_JWKS = {"keys": [{**_TEST_ALG.to_jwk(_TEST_KEY.public_key(), as_dict=True), "kid": _TEST_KID, "alg": "ES256"}]}


@pytest.fixture()
def db_session():
    """SQLite em memória — rápido, sem depender do Supabase real nos testes.

    Os models usam tipos portáveis (Uuid, defaults em Python) justamente
    para isso funcionar de forma idêntica ao Postgres real em produção.

    StaticPool + check_same_thread=False: o TestClient roda as rotas
    síncronas em outra thread (via threadpool do Starlette), e SQLite
    :memory: isola o banco por conexão/thread por padrão — sem isso, a API
    enxergaria um banco vazio mesmo com dados semeados no teste.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # SQLite ignora FKs (incluindo ON DELETE CASCADE) por padrão — sem isso,
    # o teste de cascade abaixo passaria mesmo se a migration real do
    # Postgres estivesse errada (foi assim que o achado da migration 0009
    # escapou dos testes automatizados na primeira vez).
    event.listen(engine, "connect", lambda conn, _: conn.execute("PRAGMA foreign_keys=ON"))
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session):
    """TestClient com get_db substituído pelo mesmo SQLite em memória do
    db_session, e get_jwks substituído pela chave de teste (mesmo padrão de
    dependency override) — nenhum teste bate na rede real do Supabase."""
    from app.main import app

    def override_get_db():
        yield db_session

    def override_get_jwks():
        return _TEST_JWKS

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_jwks] = override_get_jwks
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


@pytest.fixture()
def make_auth_headers():
    """Gera um Bearer token válido pro `get_current_user_id` (core/auth.py)
    aceitar — assinado com a chave EC de teste acima (`_TEST_JWKS` é o que
    o `client` fixture injeta no lugar do JWKS real do Supabase)."""

    def _make(user_id: uuid.UUID | None = None, email: str | None = None) -> tuple[uuid.UUID, dict[str, str]]:
        user_id = user_id or uuid.uuid4()
        token = jwt.encode(
            {"sub": str(user_id), "aud": "authenticated", "email": email or f"{user_id}@example.com"},
            _TEST_KEY,
            algorithm="ES256",
            headers={"kid": _TEST_KID},
        )
        return user_id, {"Authorization": f"Bearer {token}"}

    return _make
