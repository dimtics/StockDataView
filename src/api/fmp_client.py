import asyncio
from dataclasses import dataclass, field
from typing import Any

import httpx

import utils as utils
from config import settings
from models.stock_models import CombinedModel


@dataclass
class FMPClient:
    """A client for interacting with the Financial Modeling Prep API."""

    base_url: str = field(default_factory=settings.base_url)
    api_key: str = field(default_factory=settings.fmp_api_key)
    metric_types: list[str] = field(
        default_factory=lambda: [
            "profile",
            "rating",
            "quote",
            "key-metrics-ttm",
            "key-metrics",
            "financial-growth",
        ]
    )  #

    async def get_data(self, client: httpx.Client, url: str) -> dict[str, Any]:
        """Call API endpoint asynchronously"""
        response = await client.get(url)
        data = response.json()
        return data

    async def fetch_data(self, ticker: str) -> dict[str, list[dict[str, Any]]]:
        """Extracts data asynchronously from multiple FMP endpoints"""
        urls = []
        for metric in self.metric_types:
            if metric in ["profile", "quote", "rating", "key-metrics-ttm"]:
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
            replace_metric_types = {
                "rating": "ratings",
                "key-metrics": "key_metrics",
                "key-metrics-ttm": "key_metrics_ttm",
                "financial-growth": "growth",
            }  #
            new_metric_types = [
                replace_metric_types.get(item, item) for item in self.metric_types
            ]

            # Create combined records dict for validation
            records = dict(zip(new_metric_types, results))

            # Validate the combined records
            return CombinedModel(**records).model_dump()
