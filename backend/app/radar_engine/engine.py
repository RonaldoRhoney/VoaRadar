"""Radar Engine — decide se um Radar deve disparar. Puro, mesmo princípio
do app/analytics/engine.py (DEC-018 da v0.3): recebe dados, devolve um
booleano determinístico. Não conhece banco, cooldown ou notificação —
isso é responsabilidade do RadarEvaluationService (RADAR_ENGINE.md §1/§2).
"""

from dataclasses import dataclass

PRICE_BELOW = "PRICE_BELOW"
OPPORTUNITY_CLASSIFICATION = "OPPORTUNITY_CLASSIFICATION"


@dataclass(frozen=True)
class RadarCondition:
    condition_type: str
    condition_price: float | None = None
    condition_classification: str | None = None


def evaluate_radar(condition: RadarCondition, current_price: float, classification: str | None) -> bool:
    """True se a condição do Radar foi satisfeita por este preço/análise."""
    if condition.condition_type == PRICE_BELOW:
        return condition.condition_price is not None and current_price < condition.condition_price
    if condition.condition_type == OPPORTUNITY_CLASSIFICATION:
        return classification is not None and classification == condition.condition_classification
    raise ValueError(f"condition_type desconhecido: {condition.condition_type}")
