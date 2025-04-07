from config import settings
from utils import FMPClient


def test_fmp_client_initialization():
    client = FMPClient()
    assert client.base_url == settings.base_url
    assert client.api_key == settings.fmp_api_key
    assert len(client.metric_types) == 6
    assert "profile" in client.metric_types
    assert "rating" in client.metric_types
