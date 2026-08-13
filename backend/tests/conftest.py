import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.models  # noqa: F401 — registra os models na metadata do Base
from app.core.database import Base


@pytest.fixture()
def db_session():
    """SQLite em memória — rápido, sem depender do Supabase real nos testes.

    Os models usam tipos portáveis (Uuid, defaults em Python) justamente
    para isso funcionar de forma idêntica ao Postgres real em produção.
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    try:
        yield session
    finally:
        session.close()
