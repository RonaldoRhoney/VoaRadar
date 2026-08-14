import uuid
from datetime import datetime

from sqlalchemy import DateTime, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import utcnow


class Profile(Base):
    """Espelha `auth.users` (gerenciado pelo Supabase Auth) — só o mínimo
    necessário pra existir uma linha em `public` vinculável por FK
    (DATA_MODEL.md §2). Não duplica e-mail/senha, que ficam só no Auth."""

    __tablename__ = "profiles"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
