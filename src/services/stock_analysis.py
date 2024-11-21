import asyncio
import polars as pl
# from stock_valuation_app.data.fmp_client import FMPClient




raw_data = asyncio.run(extract_source_data("PAYS"))

profile_df = pl.DataFrame(raw_data["profile"])
rating_df = pl.DataFrame(raw_data["rating"])
metric_df = pl.DataFrame(raw_data["key_metrics"])
growth_df = pl.DataFrame(raw_data["growth"])

# Pivot the DataFrame
pivoted_df = profile_df.unpivot(variable_name="Column", value_name="Value")
# Sort the result to maintain the original order
pivoted_df = pivoted_df.sort("Column")

# Convert DataFrame to formatted text
formatted_text = []
for row in pivoted_df.iter_rows():
    column, value = row
    formatted_text.append(html.Div([html.Strong(f"{column}: "), f"{value}"]))

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
