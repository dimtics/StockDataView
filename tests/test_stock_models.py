from src.stock_models import (
    Growth,
    KeyMetricsTTM,
    Quote,
    Ratings,
)


class TestQuote:
    def test_valid_quote(self):
        """Test creating a valid Quote instance"""
        data = {
            "symbol": "AAPL",
            "price": 175.84,
            "changesPercentage": 0.75,
            "yearHigh": 198.23,
            "yearLow": 124.17,
            "marketCap": 2750000000000,
            "avgVolume": 55000000,
            "eps": 6.13,
            "pe": 28.7,
            "earningsAnnouncement": "2024-01-25",
            "sharesOutstanding": 15600000000,
        }

        quote = Quote(**data)
        assert quote.symbol == "AAPL"
        assert quote.price == 175.84
        assert quote.change_percent == 0.75
        assert quote.market_cap == 2750000000000

    def test_quote_with_null_values(self):
        """Test Quote with null values for optional fields"""
        data = {
            "symbol": "AAPL",
            "price": 175.84,
            "changesPercentage": None,
            "yearHigh": 198.23,
            "yearLow": 124.17,
            "marketCap": 2750000000000,
            "avgVolume": None,
            "eps": None,
            "pe": None,
            "earningsAnnouncement": "2024-01-25",
            "sharesOutstanding": 15600000000,
        }

        quote = Quote(**data)
        assert quote.change_percent is None
        assert quote.eps is None
        assert quote.pe is None


class TestRatings:
    def test_valid_ratings(self):
        """Test creating a valid Ratings instance"""
        data = {
            "symbol": "AAPL",
            "date": "2024-01-15",
            "rating": "Strong Buy",
            "ratingScore": 5,
            "ratingRecommendation": "Strong Buy",
            "ratingDetailsDCFScore": 4,
            "ratingDetailsDCFRecommendation": "Buy",
            "ratingDetailsROEScore": 5,
            "ratingDetailsROERecommendation": "Strong Buy",
            "ratingDetailsROAScore": 4,
            "ratingDetailsROARecommendation": "Buy",
            "ratingDetailsDEScore": 5,
            "ratingDetailsDERecommendation": "Strong Buy",
            "ratingDetailsPEScore": 3,
            "ratingDetailsPERecommendation": "Neutral",
            "ratingDetailsPBScore": 4,
            "ratingDetailsPBRecommendation": "Buy",
        }

        ratings = Ratings(**data)
        assert ratings.symbol == "AAPL"
        assert ratings.score == 5
        assert ratings.dcf_score == 4
        assert ratings.pe_rec == "Neutral"


class TestKeyMetricsTTM:
    def test_valid_key_metrics_ttm(self):
        """Test creating a valid KeyMetricsTTM instance"""
        data = {
            "revenuePerShareTTM": 24.87,
            "netIncomePerShareTTM": 6.13,
            "freeCashFlowPerShareTTM": 6.85,
            "peRatioTTM": 28.7,
            "enterpriseValueOverEBITDATTM": 22.5,
            "evToFreeCashFlowTTM": 25.3,
            "freeCashFlowYieldTTM": 0.039,
            "priceToSalesRatioTTM": 7.1,
            "ptbRatioTTM": 45.8,
            "pfcfRatioTTM": 25.7,
            "dividendYieldPercentageTTM": 0.0051,
            "dividendPerShareTTM": 0.92,
            "payoutRatioTTM": 0.15,
        }

        metrics = KeyMetricsTTM(**data)
        assert metrics.rev_per_share_ttm == 24.87
        assert metrics.pe_ratio_ttm == 28.7
        assert metrics.dvd_yield_pct_ttm == 0.0051

    def test_key_metrics_ttm_with_nulls(self):
        """Test KeyMetricsTTM with null values"""
        data = {
            "revenuePerShareTTM": None,
            "netIncomePerShareTTM": None,
            "freeCashFlowPerShareTTM": 6.85,
            "peRatioTTM": 28.7,
            "enterpriseValueOverEBITDATTM": None,
            "evToFreeCashFlowTTM": None,
            "freeCashFlowYieldTTM": 0.039,
            "priceToSalesRatioTTM": None,
            "ptbRatioTTM": None,
            "pfcfRatioTTM": None,
            "dividendYieldPercentageTTM": None,
            "dividendPerShareTTM": None,
            "payoutRatioTTM": None,
        }

        metrics = KeyMetricsTTM(**data)
        assert metrics.rev_per_share_ttm is None
        assert metrics.net_income_per_share_ttm is None
        assert metrics.fcf_per_share_ttm == 6.85


class TestGrowth:
    def test_valid_growth(self):
        """Test creating a valid Growth instance"""
        data = {
            "symbol": "AAPL",
            "date": "2023-12-31",
            "revenueGrowth": 0.08,
            "epsdilutedGrowth": 0.09,
            "dividendsperShareGrowth": 0.05,
            "freeCashFlowGrowth": 0.07,
            "debtGrowth": -0.02,
            "fiveYRevenueGrowthPerShare": 0.15,
            "fiveYNetIncomeGrowthPerShare": 0.18,
            "fiveYDividendperShareGrowthPerShare": 0.08,
            "fiveYOperatingCFGrowthPerShare": 0.12,
        }

        growth = Growth(**data)
        assert growth.symbol == "AAPL"
        assert growth.rev_growth == 0.08
        assert growth.fiveY_rev_growth_per_share == 0.15

    def test_growth_with_nulls(self):
        """Test Growth with null values"""
        data = {
            "symbol": "AAPL",
            "date": "2023-12-31",
            "revenueGrowth": None,
            "epsdilutedGrowth": None,
            "dividendsperShareGrowth": None,
            "freeCashFlowGrowth": 0.07,
            "debtGrowth": None,
            "fiveYRevenueGrowthPerShare": 0.15,
            "fiveYNetIncomeGrowthPerShare": None,
            "fiveYDividendperShareGrowthPerShare": None,
            "fiveYOperatingCFGrowthPerShare": None,
        }

        growth = Growth(**data)
        assert growth.rev_growth is None
        assert growth.fcf_growth == 0.07
        assert growth.fiveY_rev_growth_per_share == 0.15
