"""Motor de Price Intelligence — estatística transparente, não fabrica
inteligência. Ver docs/v0.3/PRICE_INTELLIGENCE.md.

Puro: recebe dados, devolve resultado determinístico. Não conhece banco,
API ou frontend (ARCHITECTURE.md §10/§11) — testável só com números na mão.
"""

import statistics

from app.analytics.config import CONFIDENCE_SAMPLE_SIZE_THRESHOLDS, SCORE_CLASSIFICATION_THRESHOLDS
from app.schemas.price_intelligence import Classification, ConfidenceLevel, PriceIntelligence


def classify_confidence(sample_size: int) -> ConfidenceLevel:
    for threshold, level in CONFIDENCE_SAMPLE_SIZE_THRESHOLDS:
        if sample_size >= threshold:
            return level  # type: ignore[return-value]
    return "LOW"


def classify_score(score: int) -> Classification:
    for threshold, classification in SCORE_CLASSIFICATION_THRESHOLDS:
        if score >= threshold:
            return classification  # type: ignore[return-value]
    return "VERY_EXPENSIVE"


def _score_from_position(current_price: float, minimum: float, maximum: float) -> int:
    """Quanto mais perto do mínimo histórico, maior o score — sem fórmula
    artificialmente complexa (PRICE_INTELLIGENCE.md §6)."""
    if maximum == minimum:
        return 50  # sem variação no histórico, neutro
    position = (current_price - minimum) / (maximum - minimum)
    score = round((1 - position) * 100)
    return max(0, min(100, score))


def analyze_price(current_price: float, historical_prices: list[float]) -> PriceIntelligence:
    sample_size = len(historical_prices)
    confidence = classify_confidence(sample_size)

    if sample_size == 0:
        return PriceIntelligence(
            current_price=current_price,
            sample_size=0,
            confidence=confidence,
            has_sufficient_data=False,
        )

    minimum = min(historical_prices)
    maximum = max(historical_prices)
    mean_price = statistics.mean(historical_prices)
    median_price = statistics.median(historical_prices)

    percentage_vs_mean = (current_price - mean_price) / mean_price * 100 if mean_price else None
    percentage_vs_min = (current_price - minimum) / minimum * 100 if minimum else None

    score = _score_from_position(current_price, minimum, maximum)
    classification = classify_score(score)

    return PriceIntelligence(
        current_price=current_price,
        sample_size=sample_size,
        confidence=confidence,
        has_sufficient_data=True,
        minimum=minimum,
        maximum=maximum,
        mean=round(mean_price, 2),
        median=round(median_price, 2),
        percentage_vs_mean=round(percentage_vs_mean, 1) if percentage_vs_mean is not None else None,
        percentage_vs_min=round(percentage_vs_min, 1) if percentage_vs_min is not None else None,
        score=score,
        classification=classification,
    )
