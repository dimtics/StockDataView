from dataclasses import dataclass, field
from urllib.parse import urljoin
import httpx
from typing import Any, Optional
from pydantic import BaseModel


@dataclass
class FMPClient:
    """A client for interacting with the Financial Modeling Prep API."""
    base_url: str = field(default_factory=utils.get_base_url)
    api_key: str = field(default_factory=utils.get_api_key)


    async def fetch_data(self, endpoint: str, symbol: str, period: Optional[str] = "annual"):  # params: dict[str, Any]
        """Fetch data from the Financial Modeling Prep API."""
        base_endpoint = urljoin(self.base_url, endpoint)
        if period is None:
            url = f"{base_endpoint}/{symbol}?apikey={self.api_key}"
        else:
            url = f"{base_endpoint}/{symbol}?period={period}&apikey={self.api_key}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return data