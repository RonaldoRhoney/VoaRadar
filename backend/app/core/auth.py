import time
import uuid
from dataclasses import dataclass

import httpx
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import get_settings

_bearer_scheme = HTTPBearer(auto_error=False)

FRIENDLY_UNAUTHORIZED = "Sessão inválida ou expirada. Faça login novamente."

JWKS_CACHE_TTL_SECONDS = 3600
_jwks_cache: dict[str, object] = {"keys": None, "fetched_at": 0.0}


def get_jwks() -> dict:
    """Chaves públicas de assinatura do Supabase Auth (o projeto usa chaves
    assimétricas ECC/ES256, não mais um segredo HS256 compartilhado —
    confirmado em Settings > JWT Keys do painel). Cacheado em memória por
    1h: são as mesmas chaves até uma rotação, não vale buscar a cada
    requisição. Injetável via `Depends` — os testes sobrescrevem isso pra
    não bater na rede real (mesmo padrão de `get_db`)."""
    now = time.time()
    if _jwks_cache["keys"] is None or now - _jwks_cache["fetched_at"] > JWKS_CACHE_TTL_SECONDS:
        settings = get_settings()
        response = httpx.get(f"{settings.supabase_url}/auth/v1/.well-known/jwks.json", timeout=10)
        response.raise_for_status()
        _jwks_cache["keys"] = response.json()["keys"]
        _jwks_cache["fetched_at"] = now
    return {"keys": _jwks_cache["keys"]}


def _decode_token(credentials: HTTPAuthorizationCredentials | None, jwks: dict) -> dict:
    """Nunca aceita `user_id`/e-mail vindo de body/query — a única fonte de
    verdade sobre "quem está pedindo" é a assinatura deste token
    (SECURITY.md §3)."""
    if credentials is None:
        raise HTTPException(status_code=401, detail=FRIENDLY_UNAUTHORIZED)
    try:
        header = jwt.get_unverified_header(credentials.credentials)
        key_data = next(k for k in jwks["keys"] if k["kid"] == header.get("kid"))
        signing_key = jwt.PyJWK.from_dict(key_data).key
        return jwt.decode(
            credentials.credentials,
            signing_key,
            algorithms=[key_data["alg"]],
            audience="authenticated",
        )
    except (jwt.PyJWTError, StopIteration, KeyError):
        raise HTTPException(status_code=401, detail=FRIENDLY_UNAUTHORIZED)


def _subject_uuid(payload: dict) -> uuid.UUID:
    subject = payload.get("sub")
    if subject is None:
        raise HTTPException(status_code=401, detail=FRIENDLY_UNAUTHORIZED)
    try:
        return uuid.UUID(subject)
    except ValueError:
        raise HTTPException(status_code=401, detail=FRIENDLY_UNAUTHORIZED)


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    jwks: dict = Depends(get_jwks),
) -> uuid.UUID:
    """Valida o JWT emitido pelo Supabase Auth e devolve o `user_id` (`sub`)."""
    payload = _decode_token(credentials, jwks)
    return _subject_uuid(payload)


@dataclass(frozen=True)
class CurrentUser:
    id: uuid.UUID
    email: str | None


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    jwks: dict = Depends(get_jwks),
) -> CurrentUser:
    """Igual a `get_current_user_id`, mas também expõe o e-mail (claim do
    próprio token, nunca lido de outra fonte) — usado por `/auth/me`."""
    payload = _decode_token(credentials, jwks)
    return CurrentUser(id=_subject_uuid(payload), email=payload.get("email"))
