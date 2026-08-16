"""Entrypoint pro runtime Python da Vercel — expõe o mesmo app FastAPI
que já roda local via `uvicorn app.main:app`, sem duplicar nada."""

from app.main import app  # noqa: F401
