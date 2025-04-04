from src.data_validation import get_validated_stock_data


def test_get_validated_stock_data_valid_ticker():
    """Test data validation with valid ticker"""
    ticker = "AAPL"
    data = get_validated_stock_data(ticker)

    assert data is not None
    assert "profile" in data
    assert "quote" in data
    assert "ratings" in data
    assert "key_metrics_ttm" in data
