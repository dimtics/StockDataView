import asyncio
import logging
import sys
from dataclasses import dataclass, field
from typing import Any, Optional

import httpx

from config import settings

# Define stock data type
StockData = dict[str, list[dict[str, Any]]]


def stock_logger():
    """Configures logging for stock data dashboard project"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
        force=True,  # Ensures unbuffered output
    )
    return logging.getLogger(__name__)


@dataclass
class FMPClient:
    """A client for interacting with the Financial Modeling Prep API."""

    base_url: str = settings.base_url
    api_key: str = settings.fmp_api_key
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

    async def get_data(
        self, client: httpx.Client, url: str
    ) -> Optional[dict[str, Any]]:
        """Call API endpoint asynchronously"""
        try:
            response = await client.get(url)
            data = response.json()
            return data
        except Exception as e:
            stock_logger().error(f"Error fetching data from {url}: {e}")
            return None

    async def fetch_data(self, ticker: str) -> Optional[StockData]:
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

        # Check if results are empty or contain error messages
        if isinstance(results[0], list) and len(results[0]) == 0:
            return None
        elif (
            isinstance(results[0], dict)
            and list(results[0].keys())[0] == "Error Message"
        ):
            return None
        else:
            return results
