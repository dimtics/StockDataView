# data_validation.py

import asyncio
from typing import Any, Optional

from pydantic import ValidationError

from stock_models import CombinedModel
from utils import FMPClient, StockData


async def extract_stock_data(ticker: str) -> Optional[StockData]:
    """Pulls source data from Financial Modeling Prep (FMP) API endpoints for a given ticker"""
    # Get stock data
    stock_data = await FMPClient().fetch_data(ticker)

    if stock_data:
        # Get metric types
        metric_types = FMPClient().metric_types

        # Rename some metric types to match with fields defined in the validation
        rename_metric_types: dict[Any, Any] = {
            "rating": "ratings",
            "key-metrics": "key_metrics",
            "key-metrics-ttm": "key_metrics_ttm",
            "financial-growth": "growth",
        }
        new_metric_types = [
            rename_metric_types.get(item, item) for item in metric_types
        ]

        # Create combined records dict
        records = dict(zip(new_metric_types, stock_data))
        return records


class DataValidationError(Exception):
    """Custom exception for validation error"""


def get_validated_stock_data(ticker: str) -> Optional[StockData]:
    """Validates stock data against the CombinedModel schema"""

    # Keep validation errors here
    errors: list[str] = []

    # Extract stock data
    data = asyncio.run(extract_stock_data(ticker))

    if data is None:
        return None
    else:
        # Validate stock data
        try:
            validated_data = CombinedModel(**data).model_dump()
        except ValidationError as e:
            errors.append(f"Failed validation: {str(e)}")
        if errors:
            error_message = "\n".join(errors)
            raise DataValidationError(
                f"Data validation failed with following errors: \n{error_message}"
            )
        return validated_data
