from typing import Literal

from pydantic import BaseModel

Classification = Literal["EXCELLENT", "GOOD", "NORMAL", "EXPENSIVE", "VERY_EXPENSIVE"]
ConfidenceLevel = Literal["LOW", "MEDIUM", "HIGH"]


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
