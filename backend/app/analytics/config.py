"""Limiares do Analytics Engine — centralizados aqui, não espalhados pelo
código (PRICE_INTELLIGENCE.md §13). Ajustáveis sem tocar na lógica."""

# score -> classificação, do maior limiar pro menor.
SCORE_CLASSIFICATION_THRESHOLDS: list[tuple[int, str]] = [
    (80, "EXCELLENT"),
    (60, "GOOD"),
    (40, "NORMAL"),
    (20, "EXPENSIVE"),
    (0, "VERY_EXPENSIVE"),
]

# sample_size -> nível de confiança.
CONFIDENCE_SAMPLE_SIZE_THRESHOLDS: list[tuple[int, str]] = [
    (30, "HIGH"),
    (10, "MEDIUM"),
    (0, "LOW"),
]
