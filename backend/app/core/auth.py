import uuid

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import get_settings

_bearer_scheme = HTTPBearer(auto_error=False)

FRIENDLY_UNAUTHORIZED = "Sessão inválida ou expirada. Faça login novamente."


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
) -> uuid.UUID:
    """Valida o JWT emitido pelo Supabase Auth e devolve o `user_id` (`sub`).

    Nunca aceita `user_id` vindo de body/query — a única fonte de verdade
    sobre "quem está pedindo" é a assinatura deste token (SECURITY.md §3).
    """
    if credentials is None:
        raise HTTPException(status_code=401, detail=FRIENDLY_UNAUTHORIZED)

    settings = get_settings()
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            audience="authenticated",
        )
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail=FRIENDLY_UNAUTHORIZED)

    subject = payload.get("sub")
    if subject is None:
        raise HTTPException(status_code=401, detail=FRIENDLY_UNAUTHORIZED)

    try:
        return uuid.UUID(subject)
    except ValueError:
        raise HTTPException(status_code=401, detail=FRIENDLY_UNAUTHORIZED)
