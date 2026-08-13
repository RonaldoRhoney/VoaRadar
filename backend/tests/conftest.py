import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401 — registra os models na metadata do Base
from app.core.database import Base, get_db


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
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session):
    """TestClient com get_db substituído pelo mesmo SQLite em memória do
    db_session — permite semear dados via repository e depois bater na API."""
    from app.main import app

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
