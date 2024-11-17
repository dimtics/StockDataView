import asyncio
from stock_valuation_app.data import fmp_client

async def main() -> None:
    """Main function to fetch data from the Financial Modeling Prep API."""
    api_client = fmp_client.FMPClient()
    rating_endpoint = fmp_client.get_endpoint("annual_ratios")
    data = await api_client.fetch_data(rating_endpoint, "AAPL")
    print(data)


if __name__ == "__main__":
    asyncio.run(main())
