from app.analytics.engine import analyze_price, classify_confidence, classify_score


class TestNoData:
    def test_empty_history_has_insufficient_data(self):
        result = analyze_price(current_price=500, historical_prices=[])

        assert result.has_sufficient_data is False
        assert result.confidence == "LOW"
        assert result.score is None
        assert result.classification is None
        assert result.minimum is None
        assert result.mean is None


class TestStatistics:
    def test_minimum_maximum_mean_median(self):
        result = analyze_price(current_price=500, historical_prices=[400, 500, 600, 900])

        assert result.minimum == 400
        assert result.maximum == 900
        assert result.mean == 600.0
        assert result.median == 550.0

    def test_median_is_not_skewed_by_an_outlier_like_mean_is(self):
        # 4 preços normais + 1 outlier bem acima — mediana deve continuar
        # perto do "normal", média sim é puxada pra cima.
        prices = [400, 420, 430, 440, 5000]
        result = analyze_price(current_price=430, historical_prices=prices)

        assert result.median == 430
        assert result.mean > 1000  # puxado pelo outlier
        assert result.median < result.mean

    def test_percentage_vs_mean_and_min(self):
        result = analyze_price(current_price=429, historical_prices=[429, 620])

        assert result.mean == 524.5
        assert result.percentage_vs_mean == round((429 - 524.5) / 524.5 * 100, 1)
        assert result.percentage_vs_min == 0.0  # é o próprio mínimo


class TestScore:
    def test_price_at_minimum_scores_100(self):
        result = analyze_price(current_price=399, historical_prices=[399, 620, 890])
        assert result.score == 100
        assert result.classification == "EXCELLENT"

    def test_price_at_maximum_scores_0(self):
        result = analyze_price(current_price=890, historical_prices=[399, 620, 890])
        assert result.score == 0
        assert result.classification == "VERY_EXPENSIVE"

    def test_price_at_midpoint_scores_50(self):
        result = analyze_price(current_price=500, historical_prices=[0, 1000])
        assert result.score == 50
        assert result.classification == "NORMAL"

    def test_no_variation_in_history_is_neutral(self):
        result = analyze_price(current_price=500, historical_prices=[500, 500, 500])
        assert result.score == 50

    def test_current_price_above_historical_max_clamps_to_zero(self):
        result = analyze_price(current_price=2000, historical_prices=[400, 600])
        assert result.score == 0

    def test_current_price_below_historical_min_clamps_to_hundred(self):
        result = analyze_price(current_price=100, historical_prices=[400, 600])
        assert result.score == 100


class TestClassificationBoundaries:
    def test_score_boundaries_map_to_expected_classification(self):
        assert classify_score(100) == "EXCELLENT"
        assert classify_score(80) == "EXCELLENT"
        assert classify_score(79) == "GOOD"
        assert classify_score(60) == "GOOD"
        assert classify_score(59) == "NORMAL"
        assert classify_score(40) == "NORMAL"
        assert classify_score(39) == "EXPENSIVE"
        assert classify_score(20) == "EXPENSIVE"
        assert classify_score(19) == "VERY_EXPENSIVE"
        assert classify_score(0) == "VERY_EXPENSIVE"


class TestConfidenceBoundaries:
    def test_sample_size_boundaries_map_to_expected_confidence(self):
        assert classify_confidence(0) == "LOW"
        assert classify_confidence(9) == "LOW"
        assert classify_confidence(10) == "MEDIUM"
        assert classify_confidence(29) == "MEDIUM"
        assert classify_confidence(30) == "HIGH"
        assert classify_confidence(1000) == "HIGH"

    def test_low_sample_size_still_computes_stats_but_flags_low_confidence(self):
        # Poucos dados não é "sem dados": ainda calcula, só com confiança
        # baixa — a interface (FASE 8) que decide como comunicar isso.
        result = analyze_price(current_price=500, historical_prices=[400, 600])

        assert result.has_sufficient_data is True
        assert result.confidence == "LOW"
        assert result.sample_size == 2
        assert result.score is not None


class TestDeterminism:
    def test_same_input_always_produces_the_same_output(self):
        first = analyze_price(current_price=429, historical_prices=[399, 429, 620, 890])
        second = analyze_price(current_price=429, historical_prices=[399, 429, 620, 890])

        assert first == second
