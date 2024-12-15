import asyncio
import duckdb as db
from typing import Any, Optional
import polars as pl
import streamlit as st
from stock_valuation_app.api.fmp_client import FMPClient



# async def extract_source_data(ticker: str):
#     source_data = await FMPClient().fetch_data(ticker)
#     return source_data


# raw_data = asyncio.run(extract_source_data("PAYS"))

# profile_df = pl.DataFrame(raw_data["profile"])

StockData = dict[str, list[dict[str, Any]]]

#@st.cache_resource
async def extract_source_data(ticker: str) -> StockData:
    """Pull source data for a given ticker"""
    source_data = await FMPClient().fetch_data(ticker)
    return source_data


def get_long_df(df: pl.DataFrame, var: str, value: str) -> pl.DataFrame:
    """Convert wide dataframe to long format"""
    longdf = df.unpivot(variable_name=var, value_name=value)
    return longdf


#@st.cache_data
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
                """
        ).pl()
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
                """
            ).pl()
    return ndf

#@st.cache_data
def transform_ratios(stock_data: StockData):
    """Processes ratios dataset"""

    df = pl.DataFrame(stock_data.get("ratios", None)).cast(pl.String())

    # if df is None:
    #     print("Dataframe is empty")
    #     return None

    xdf = db.sql("""WITH ref_data AS (SELECT * EXCLUDE (symbol, pb_ratio, curr_ratio) FROM df) UNPIVOT ref_data ON COLUMNS(* EXCLUDE year) INTO NAME metric VALUE values; """).pl()
    return xdf

    # if not df.is_empty():
    #     newdf = df.select(pl.exclude(["symbol", "book_val_per_share"]))
    #     val_var = newdf.select(pl.exclude(["year"])).columns
    #     idx = newdf.select(pl.col("year")).columns
    #     long_newdf = newdf.unpivot(on=val_var, index=idx, variable_name="Metric", value_name="Value")
    #     return (long_newdf, val_var)




# data = asyncio.run(extract_source_data('NVDA'))
# xdf = transform_ratios(data)
# # # print(xdf.schema)
# # # print()
# print(xdf.head(10))
# # xdf, val_var = transform_ratios(data)
# # print(xdf.head())
# # print(val_var)

# df = pl.DataFrame(data.get("ratios", None))
# print(df.lazy().collect().schema)

# profile_df = pl.DataFrame(raw_data["profile"])
# rating_df = pl.DataFrame(raw_data["rating"])
# metric_df = pl.DataFrame(raw_data["key_metrics"])
# growth_df = pl.DataFrame(raw_data["growth"])

# # Pivot the DataFrame
# pivoted_df = profile_df.unpivot(variable_name="Column", value_name="Value")
# # Sort the result to maintain the original order
# pivoted_df = pivoted_df.sort("Column")

# # Convert DataFrame to formatted text
# formatted_text = []
# for row in pivoted_df.iter_rows():
#     column, value = row
#     formatted_text.append(html.Div([html.Strong(f"{column}: "), f"{value}"]))

# async def extract_source_data(ticker: str):
#     source_data = await FMPClient().fetch_data(ticker)
#     return {
#         "profile": source_data["profile"],
#         "rating": source_data["rating"],
#         "key_metrics": source_data["key_metrics"],
#         "growth": source_data["growth"],
#     }

# async def extract_source_data(ticker: str):
#     source_data = await FMPClient().fetch_data(ticker)
#     return source_data


# if __name__ == "__main__":
#     pass
    # raw_data = asyncio.run(extract_source_data('PAYS'))

    # def get_dataframes():
    #     """Captures source dataframes"""
    #     profile_df = pl.DataFrame(raw_data["profile"])
    #     rating_df = pl.DataFrame(raw_data["rating"])
    #     metric_df = pl.DataFrame(raw_data["key_metrics"])
    #     growth_df = pl.DataFrame(raw_data["growth"])
    #     return (profile_df, rating_df, metric_df, growth_df)
