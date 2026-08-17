from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import admin, airports, auth, flights, health, notifications, price_intelligence, radars
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(flights.router)
app.include_router(price_intelligence.router)
app.include_router(auth.router)
app.include_router(airports.router)
app.include_router(radars.router)
app.include_router(notifications.router)
app.include_router(admin.router)
