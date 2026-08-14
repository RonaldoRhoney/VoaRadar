import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import utcnow

USER = "user"
ADMIN = "admin"


class Profile(Base):
    """Espelha `auth.users` (gerenciado pelo Supabase Auth) — só o mínimo
    necessário pra existir uma linha em `public` vinculável por FK
    (DATA_MODEL.md §2). Não duplica e-mail/senha, que ficam só no Auth.

    A linha é criada pelo trigger `handle_new_user()` (migration 0011),
    não pelo backend — cobre cadastro por e-mail/senha e por OAuth
    (Google) de forma uniforme, já promovendo `rhoneyinc@gmail.com` a
    `admin` automaticamente (skill RhoneyInc `admin-padrao`)."""

    __tablename__ = "profiles"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    role: Mapped[str] = mapped_column(String(16), default=USER)
