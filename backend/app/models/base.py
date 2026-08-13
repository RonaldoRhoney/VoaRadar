import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class TimestampedModel(Base):
    """Base com id/created_at portáveis (Uuid + default em Python, não
    gen_random_uuid()/now() do Postgres) — assim os models rodam idênticos
    contra SQLite em memória nos testes e contra o Supabase em produção."""

    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
