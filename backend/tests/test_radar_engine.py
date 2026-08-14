import pytest

from app.radar_engine.engine import (
    OPPORTUNITY_CLASSIFICATION,
    PRICE_BELOW,
    RadarCondition,
    evaluate_radar,
)


class TestPriceBelow:
    def test_disparo_quando_preco_abaixo_do_limite(self):
        condition = RadarCondition(condition_type=PRICE_BELOW, condition_price=500)

        assert evaluate_radar(condition, current_price=429, classification="GOOD") is True

    def test_nao_dispara_quando_preco_igual_ao_limite(self):
        condition = RadarCondition(condition_type=PRICE_BELOW, condition_price=500)

        assert evaluate_radar(condition, current_price=500, classification=None) is False

    def test_nao_dispara_quando_preco_acima_do_limite(self):
        condition = RadarCondition(condition_type=PRICE_BELOW, condition_price=500)

        assert evaluate_radar(condition, current_price=600, classification=None) is False


class TestOpportunityClassification:
    def test_disparo_quando_classificacao_bate(self):
        condition = RadarCondition(condition_type=OPPORTUNITY_CLASSIFICATION, condition_classification="EXCELLENT")

        assert evaluate_radar(condition, current_price=429, classification="EXCELLENT") is True

    def test_nao_dispara_quando_classificacao_diferente(self):
        condition = RadarCondition(condition_type=OPPORTUNITY_CLASSIFICATION, condition_classification="EXCELLENT")

        assert evaluate_radar(condition, current_price=429, classification="GOOD") is False

    def test_nao_dispara_quando_classificacao_ausente(self):
        condition = RadarCondition(condition_type=OPPORTUNITY_CLASSIFICATION, condition_classification="EXCELLENT")

        assert evaluate_radar(condition, current_price=429, classification=None) is False


class TestConditionTypeInvalido:
    def test_levanta_valueerror(self):
        condition = RadarCondition(condition_type="ALGO_DESCONHECIDO")

        with pytest.raises(ValueError):
            evaluate_radar(condition, current_price=429, classification=None)
