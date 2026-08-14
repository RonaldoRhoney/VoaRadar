from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Voa Radar API"
    environment: str = "development"
    cors_origins: list[str] = ["http://localhost:5173"]
    database_url: str = ""

    # Supabase Auth (v0.4) — mesmo projeto Supabase já usado pro banco.
    # supabase_url: endpoint REST do projeto (ex: https://xxxx.supabase.co).
    # supabase_anon_key: chave pública, usada nas chamadas de signup/login.
    # supabase_jwt_secret: segredo HS256 do projeto (Settings > API > JWT Secret),
    # usado só pra VALIDAR o token recebido — nunca pra assinar nada aqui.
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_jwt_secret: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
