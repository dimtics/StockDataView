import duckdb as db
from typing import Any
import polars as pl
from api.fmp_client import FMPClient


StockData = dict[str, list[dict[str, Any]]]


# @st.cache_resource
async def extract_source_data(ticker: str) -> StockData:
    """Pull source data for a given ticker"""
    source_data = await FMPClient().fetch_data(ticker)
    return source_data


def get_long_df(df: pl.DataFrame, var: str, value: str) -> pl.DataFrame:
    """Convert wide dataframe to long format"""
    longdf = df.unpivot(variable_name=var, value_name=value)
    return longdf


# @st.cache_data
def transform_profile(stock_data: StockData):
    """Processes profile dataset"""
    df = pl.DataFrame(stock_data.get("profile", None)).cast(pl.String())

    if df is None:
        print("Dataframe is empty")
        return None

    ndf = db.sql("""WITH ref_data AS (SELECT symbol AS Symbol, price AS Price, beta AS Beta,
                 vol_avg AS 'Average Volume', mkt_cap AS 'Market Cap', last_div AS 'Last Dividend',
                 low_high AS '52w Low - High', price_change AS 'Price Change', currency AS Currency,
                 exchange AS Exchange, sector AS Sector, industry AS Industry, description AS Description
                 FROM df
                )
                UNPIVOT ref_data
                ON COLUMNS(*)
                INTO
                    NAME metric
                    VALUE values
                """).pl()
    result_dict = dict(zip(ndf["metric"], ndf["values"]))
    return result_dict


# @st.cache_data
def transform_rating(stock_data: StockData):
    """Processes rating dataset"""
    df = pl.DataFrame(stock_data.get("ratings", None)).cast(pl.String())

    if df is None:
        print("Dataframe is empty")
        return None

    ndf = db.sql("""WITH ref_data AS (SELECT symbol AS Symbol, date AS Date, rating AS Rating, score AS Score,
                 recommendation AS Recommendation, dcf_score AS 'DCF Score', dcf_rec AS 'DCF Recommendation',
                 roe_score AS 'ROE Score', roe_rec AS 'ROE Recommendation', roa_score AS 'ROA Score',
                 roa_rec AS 'ROA Recommendation', de_score AS 'DE Score', de_rec AS 'DE Recommendation',
                 pe_score AS 'PE Score', pe_rec AS 'PE Recommendation', pb_score AS 'PB Score',
                 pb_rec AS 'PB Recommendation'
                 FROM df
                 )
                 UNPIVOT ref_data
                 ON COLUMNS(*)
                 INTO
                    NAME 'Metric'
                    VALUE Rating
                """).pl()
    return ndf


# @st.cache_data
def transform_ratios(stock_data: StockData):
    """Processes ratios dataset"""

    df = pl.DataFrame(stock_data.get("ratios", None)).cast(pl.String())

    # if df is None:
    #     print("Dataframe is empty")
    #     return None

    xdf = db.sql(
        """WITH ref_data AS (SELECT * EXCLUDE (symbol, pb_ratio, curr_ratio) FROM df) UNPIVOT ref_data ON COLUMNS(* EXCLUDE year) INTO NAME metric VALUE values; """
    ).pl()
    return xdf
