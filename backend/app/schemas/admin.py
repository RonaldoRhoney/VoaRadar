from pydantic import BaseModel


class PlatformMetrics(BaseModel):
    """Só agregados — nunca dado individual de um usuário específico
    (mesmo princípio de minimização já aplicado no FinTra: um painel admin
    não precisa, e não deve, expor a rota/preço que uma pessoa está
    monitorando pra outro usuário ver)."""

    total_users: int
    total_radars: int
    active_radars: int
    total_radar_events: int
    total_notifications: int
    new_users_7d: int
    new_radars_7d: int
