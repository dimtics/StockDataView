from fastapi import APIRouter, Depends
from ..data.fmp_client import FMPClient
from ..services.valuation import (
    calculate_growth_rates,
    is_quality_dividend_growth_stock,
    is_undervalued,
)

router = APIRouter()


async def get_fmp_client():
    return FMPClient("YOUR_API_KEY")


@router.get("/stock/{symbol}")
async def get_stock_valuation(
    symbol: str, fmp_client: FMPClient = Depends(get_fmp_client)
):
    financial_data = await fmp_client.get_financial_data(symbol)
    growth_rates = calculate_growth_rates(financial_data)

    # Assuming we have a way to get the current P/E ratio
    current_pe = 15  # This should be fetched from the API

    return {
        "symbol": symbol,
        "growth_rates": growth_rates,
        "is_quality_dividend_growth_stock": is_quality_dividend_growth_stock(
            growth_rates
        ),
        "is_undervalued": is_undervalued(growth_rates, current_pe),
    }
