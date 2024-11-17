import os
import asyncio
from dataclasses import dataclass, field
from typing import Any
import httpx
import utils
from stock_valuation_app.models.stock import CombinedModel


def get_endpoint(url: str) -> str:
    """Get endpoints from the configuration."""
    api_config = utils.get_section_config("api")
    return api_config.get(f"{url}")


def get_base_url() -> str:
    """Get the base URL from the configuration."""
    return get_endpoint("base_url")


def get_api_key() -> str:
    """Get the API key from the .env file."""
    return os.getenv("FMP_API_KEY", "")


@dataclass
class FMPClient:
    """A client for interacting with the Financial Modeling Prep API."""
    base_url: str = field(default_factory=get_base_url)
    api_key: str = field(default_factory=get_api_key)
    metric_types: list[str] = field(default_factory=lambda: ["profile", "rating", "ratios", "key-metrics", "financial-growth",])

    async def get_data(self, client: httpx.Client, url: str) -> dict[str, Any]:
        """Call API endpoint asynchronously"""
        response = await client.get(url)
        data = response.json()
        return data

    async def fetch_data(self, ticker: str) -> dict[str, list[dict[str, Any]]]:
        urls = []
        for metric in self.metric_types:
            if metric in ["profile", "rating"]:
                endpoint = f"{self.base_url}/{metric}/{ticker}?apikey={self.api_key}"
            else:
                endpoint = f"{self.base_url}/{metric}/{ticker}?period=annual&apikey={self.api_key}"
            urls.append(endpoint)

        async with httpx.AsyncClient() as client:
            tasks = []
            for url in urls:
                tasks.append(asyncio.create_task(self.get_data(client, url)))

            results = await asyncio.gather(*tasks)

            # Rename some metric types to match with fields defined in the CombinedModel
            replace_metric_types = {"key-metrics": "key_metrics", "financial-growth": "growth",}
            new_metric_types = [replace_metric_types.get(item, item) for item in self.metric_types]

            # Create combined records dict for validation
            records = dict(zip(new_metric_types, results))

            # Validate the combined records
            return CombinedModel(**records).model_dump()
