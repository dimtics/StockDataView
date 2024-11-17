import asyncio
import polars as pl
from stock_valuation_app.data.fmp_client import FMPClient



async def extract_source_data(ticker: str):
    source_data = await FMPClient().fetch_data(ticker)
    return source_data

if __name__ == "__main__":
    raw_data = asyncio.run(extract_source_data('PAYS'))

    profile_df = pl.DataFrame(raw_data["profile"])
    rating_df = pl.DataFrame(raw_data["rating"])
    metric_df = pl.DataFrame(raw_data["key_metrics"])
    growth_df = pl.DataFrame(raw_data["growth"])

    print(profile_df.head())
    print(rating_df.head())
    print(metric_df.head())
    print(growth_df.head())