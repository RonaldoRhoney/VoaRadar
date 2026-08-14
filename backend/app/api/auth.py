import uuid

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.repositories.profile_repository import ProfileRepository
from app.schemas.auth import LoginRequest, SignupRequest, TokenResponse

_bearer_scheme = HTTPBearer(auto_error=False)

router = APIRouter(prefix="/auth", tags=["auth"])

FRIENDLY_AUTH_ERROR = "Não foi possível completar essa ação. Confira o e-mail e a senha e tente de novo."
CONFIRMATION_REQUIRED = "Cadastro recebido. Confirme seu e-mail para poder entrar."


def _auth_headers() -> dict[str, str]:
    settings = get_settings()
    return {"apikey": settings.supabase_anon_key, "Content-Type": "application/json"}


@router.post("/signup", response_model=TokenResponse | dict[str, str])
def signup(payload: SignupRequest, db: Session = Depends(get_db)) -> TokenResponse | dict[str, str]:
    """Delega o cadastro pro Supabase Auth — o backend nunca guarda senha.
    A linha em `profiles` é criada aqui mesmo, pela conexão do backend (que
    bypassa RLS), não por INSERT vindo do cliente autenticado."""
    settings = get_settings()
    response = httpx.post(
        f"{settings.supabase_url}/auth/v1/signup",
        json={"email": payload.email, "password": payload.password},
        headers=_auth_headers(),
        timeout=10,
    )
    if response.status_code >= 400:
        raise HTTPException(status_code=400, detail=FRIENDLY_AUTH_ERROR)

    body = response.json()
    user_id = (body.get("user") or body).get("id")
    if user_id is not None:
        ProfileRepository(db).get_or_create(uuid.UUID(user_id))
        db.commit()

    return _to_token_response(body)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    settings = get_settings()
    response = httpx.post(
        f"{settings.supabase_url}/auth/v1/token?grant_type=password",
        json={"email": payload.email, "password": payload.password},
        headers=_auth_headers(),
        timeout=10,
    )
    if response.status_code >= 400:
        raise HTTPException(status_code=401, detail=FRIENDLY_AUTH_ERROR)
    body = response.json()
    if "access_token" not in body:
        raise HTTPException(status_code=401, detail=FRIENDLY_AUTH_ERROR)
    return TokenResponse(access_token=body["access_token"], refresh_token=body["refresh_token"], expires_in=body["expires_in"])


@router.post("/logout", status_code=204)
def logout(credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme)) -> None:
    """Revoga o refresh token no Supabase Auth. Idempotente: mesmo sem
    sessão válida, sempre responde 204 — logout nunca deveria falhar
    visivelmente pro usuário."""
    if credentials is None:
        return
    settings = get_settings()
    httpx.post(
        f"{settings.supabase_url}/auth/v1/logout",
        headers={**_auth_headers(), "Authorization": f"Bearer {credentials.credentials}"},
        timeout=10,
    )


def _to_token_response(body: dict) -> TokenResponse | dict[str, str]:
    """O Supabase Auth pode responder sem sessão no cadastro (confirmação de
    e-mail pendente, comportamento padrão do projeto) — nesse caso não há
    token pra devolver, só um aviso amigável."""
    if "access_token" not in body:
        return {"status": "confirmation_required", "message": CONFIRMATION_REQUIRED}
    return TokenResponse(access_token=body["access_token"], refresh_token=body["refresh_token"], expires_in=body["expires_in"])
