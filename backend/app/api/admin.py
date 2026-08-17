from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.auth import CurrentUser, get_current_user
from app.core.database import get_db
from app.models import Notification, Profile, Radar, RadarEvent
from app.models.base import utcnow
from app.models.radar import ACTIVE
from app.repositories.profile_repository import ProfileRepository
from app.schemas.admin import PlatformMetrics

router = APIRouter(prefix="/admin", tags=["admin"])

FRIENDLY_FORBIDDEN = "Acesso restrito a administradores."


def require_admin(current_user: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)) -> CurrentUser:
    """`role` só é decidido a partir de `profiles`, nunca de claim do token
    (mesmo princípio de `/auth/me`, `api/auth.py`) — o JWT prova quem é o
    usuário, não o que ele pode fazer."""
    profile = ProfileRepository(db).get_or_create(current_user.id)
    db.commit()
    if profile.role != "admin":
        raise HTTPException(status_code=403, detail=FRIENDLY_FORBIDDEN)
    return current_user


@router.get("/metrics", response_model=PlatformMetrics)
def get_platform_metrics(
    _admin: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db),
) -> PlatformMetrics:
    """Só agregados (docs/foundation equivalente do FinTra: minimização) —
    nunca expõe qual rota/preço um usuário específico está monitorando."""
    since = utcnow() - timedelta(days=7)

    return PlatformMetrics(
        total_users=db.scalar(select(func.count()).select_from(Profile)) or 0,
        total_radars=db.scalar(select(func.count()).select_from(Radar)) or 0,
        active_radars=db.scalar(select(func.count()).select_from(Radar).where(Radar.status == ACTIVE)) or 0,
        total_radar_events=db.scalar(select(func.count()).select_from(RadarEvent)) or 0,
        total_notifications=db.scalar(select(func.count()).select_from(Notification)) or 0,
        new_users_7d=db.scalar(select(func.count()).select_from(Profile).where(Profile.created_at >= since)) or 0,
        new_radars_7d=db.scalar(select(func.count()).select_from(Radar).where(Radar.created_at >= since)) or 0,
    )
