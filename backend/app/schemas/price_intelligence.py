from datetime import datetime
from typing import Literal

from pydantic import BaseModel

Classification = Literal["EXCELLENT", "GOOD", "NORMAL", "EXPENSIVE", "VERY_EXPENSIVE"]
ConfidenceLevel = Literal["LOW", "MEDIUM", "HIGH"]


class PriceHistoryPoint(BaseModel):
    price: float
    observed_at: datetime


class PriceIntelligence(BaseModel):
    current_price: float
    sample_size: int
    confidence: ConfidenceLevel
    has_sufficient_data: bool

    minimum: float | None = None
    maximum: float | None = None
    mean: float | None = None
    median: float | None = None
    percentage_vs_mean: float | None = None
    percentage_vs_min: float | None = None
    score: int | None = None
    classification: Classification | None = None

    # Só pro gráfico (UX.md §5) — a análise em si usa as estatísticas acima,
    # não essa série crua.
    history: list[PriceHistoryPoint] = []
