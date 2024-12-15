from typing import Any
import asyncio
import pandas as pd
import duckdb as db
import polars as pl
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.express as px
from stock_valuation_app.services.stock_analysis import extract_source_data


def display_profile(profile_data: dict[str, Any]):
    """Display company profile in sidebar"""
    try:
        if profile_data:
            st.sidebar.write("## Company Profile")
            st.sidebar.image(profile_data["image"], width=180)
            st.sidebar.write(f"## {profile_data['company_name']}")
            st.sidebar.write(f"**Sector**: {profile_data['sector']}")
            st.sidebar.write(f"**Industry**: {profile_data['industry']}")
            st.sidebar.write(f"**Description**: {profile_data['description']}")
    except IndexError:
        st.write("Couldn't find company profile.")


def display_quotes(quote_data: dict[str, Any], profile_data: dict[str, Any]):

    def display_stock_metric(header, value):
        html_content = f"""
            <style>
            .stock-box {{
                background-color: #f0f0f0;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                padding: 0.5px;
                margin-bottom: 0.5px;
                width: 160px;
                border: 1px solid #e0e0e0;
                text-align: center;
            }}
            .metric-header {{
                font-size: 17px;
                color: #7f8c8d;
                margin-bottom: 1px;
            }}
            .metric-value {{
                font-size: 19px;
                color: #174C4F;
            }}
            </style>
            <div class="stock-box">
                <div class="metric-header">{header}</div>
                <div class="metric-value">{value}</div>
            </div>
        """
        st.html(html_content)
    try:
        #label = quote_data["symbol"]
        stock_price = f"${quote_data['price']:,.2f}"
        change_price = f"{quote_data['change_percent']:,.2f}%"
        year_low = f"${quote_data['year_low']:,.2f}"
        year_high = f"${quote_data['year_high']:,.2f}"
        market_cap = f"{quote_data["market_cap"]/1_000_000_000:.2f}B"
        vol_avg = f"{quote_data["vol_avg"]/1_000_000:.2f}M"
        earning_date = quote_data["earning_date"][:10]
        shares_outstanding = f"{quote_data["shares_outstanding"]/1_000_000_000:.2f}B"
        beta = profile_data["beta"]

        col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)

        with col1:
            display_stock_metric("Price", stock_price)
        with col2:
            display_stock_metric("Change Percent", change_price)
        with col3:
            display_stock_metric("52w Low", year_low)
        with col4:
            display_stock_metric("52w High", year_high)
        with col5:
            display_stock_metric("Avg Volume", vol_avg)
        with col6:
            display_stock_metric("Market Cap", market_cap)
        with col7:
            display_stock_metric("Shares", shares_outstanding)
        with col8:
            display_stock_metric("Beta", beta)
        with col9:
            display_stock_metric("Earning Date", earning_date)
    except Exception as e:
        print(e)


def display_metric_tables(data: list[dict[str, Any]]):

    def generate_table_rows(data: dict[str, Any]):  # table_name: str
        rows_html = ""
        for metric, value in data.items():
            row = f"""
                <style>
                .row {{
                    display: flex;
                    justify-content: space-between;
                    border-bottom: 1px solid #e0e0e0;
                    padding: 8px 0;
                }}
                .metric {{
                    font-size: 15px;
                    color: #888;
                    text-align: left;
                }}
                .value {{
                    font-size: 15px;
                    color: #333;
                    text-align: right;
                }}
                </style>
                <div class="row">
                    <span class="metric">{metric}:</span>
                    <span class="value">{value}</span>
                </div>
                """
            rows_html += row
        return rows_html

    def display_table(data: dict[str, Any], header_name: str):
        table_html = f"""
            <style>
                .compact-table {{
                    font-family: Arial, sans-serif;
                    width: 250px;
                }}
                .header {{
                    font-size: 18px;
                    font-weight: bold;
                    border-bottom: 1px solid #e0e0e0;
                    padding: 8px 0;
                }}
            </style>
            <div class="compact-table">
                <div class="header">{header_name}</div>
                {generate_table_rows(data)}
            </div>
            """
        return components.html(table_html, height=210) #210



    # Get data and generate tables
    quote_data, key_metrics_ttm_data, growth_data, ratings_data = data
    latest_growth_data = growth_data[0]
    latest_ratings_data = ratings_data[0]

    valuation_data = {
        "PE Ratio (TTM)": f"{quote_data['pe']:,.2f}",
        "EPS (TTM)": f"{quote_data['eps']:,.2f}",
        "EV/EBITDA (TTM)": f"{key_metrics_ttm_data['ev_over_ebitda_ttm']:,.2f}",
        "Price/Sales (TTM)": f"{key_metrics_ttm_data['pts_ratio_ttm']:,.2f}",
        "Price/Book (TTM)": f"{key_metrics_ttm_data['ptb_ratio_ttm']:,.2f}",
    }

    freecashflow_data = {
        "FCF Yield (TTM)": f"{key_metrics_ttm_data['fcf_yield_ttm'] * 100:,.2f}%",
        "Price/FCF (TTM)": f"{key_metrics_ttm_data['pfcf_ratio_ttm']:,.2f}",
        "EV/FCF (TTM)": f"{key_metrics_ttm_data['ev_to_fcf_ttm']:,.2f}",
        "FCF/Share (TTM)": f"{key_metrics_ttm_data['fcf_per_share_ttm']:,.2f}",
    }
    growth_metric_data = {
        "5Y Rev Growth/Share": f"{latest_growth_data['fiveY_rev_growth_per_share']:,.2f}",
        "5Y NI Growth/Share": f"{latest_growth_data['fiveY_ni_growth_per_share']:,.2f}",
        "5Y Div Growth/Share": f"{latest_growth_data['fiveY_dps_growth_per_share']:,.2f}",
        "5Y OCF Growth/Share": f"{latest_growth_data['fiveY_opcf_growth_per_share']:,.2f}",
    }

    dividend_data = {
        "Div Yield (TTM)": f"{key_metrics_ttm_data['dvd_yield_pct_ttm']:,.2f}%",
        "Div/Share (TTM)": f"{key_metrics_ttm_data['dvd_per_share_ttm']:,.2f}",
        "Payout Ratio (TTM)": f"{key_metrics_ttm_data['payout_ratio_ttm'] * 100:,.2f}%",
    }

    rating_data = {
        #"Symbol": f"{latest_ratings_data['symbol']}",
        "Date": f"{latest_ratings_data['date']}",
        "Rating": f"{latest_ratings_data['rating']}",
        "Score": f"{latest_ratings_data['score']}",
        "Recommendation": f"{latest_ratings_data['recommendation']}",
    }

    # Define tables layout
    container = st.empty()
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        container.markdown(
            display_table(valuation_data, "Valuation"), unsafe_allow_html=True
        )
    with col2:
        container.markdown(
            display_table(freecashflow_data, "Cash Flow"), unsafe_allow_html=True
        )
    with col3:
        container.markdown(
            display_table(growth_metric_data, "Growth"), unsafe_allow_html=True
        )
    with col4:
        container.markdown(
            display_table(dividend_data, "Dividend"), unsafe_allow_html=True
        )
    with col5:
        container.markdown(
            display_table(rating_data, "Rating"), unsafe_allow_html=True
        )


# def display_ratings(ratings_data: list[dict[str, Any]]):
#     """Displays rating dataset"""

#     dfx = pl.DataFrame(ratings_data).cast(pl.String())

#     if dfx is None:
#         print("Dataframe is empty")
#         return None

#     ndf = db.sql("""SELECT symbol AS Symbol, date AS Date, rating AS Rating, score AS Score,
#                 recommendation AS Recommendation, CONCAT(dcf_score, ' ', '(', dcf_rec, ')') AS 'Discounted Cash Flow',
#                 CONCAT(roe_score, ' ', '(', roe_rec, ')') AS 'Return on Equity',
#                 CONCAT(roa_score, ' ', '(', roa_rec, ')') AS 'Return on Assets',
#                 CONCAT(de_score, ' ', '(', de_rec, ')') AS 'Debt-to-Equity',
#                 CONCAT(pe_score, ' ', '(', pe_rec, ')') AS 'Price-to-Earnings',
#                 CONCAT(pb_score, ' ', '(', pb_rec, ')') AS 'Price-to-Book'
#                 FROM dfx
#                 """).df()

#     # Define custom CSS for larger text and center alignment
#     custom_css = """
#         <style>
#             .dataframe {
#                 font-size: 20px !important;
#             }
#             .dataframe th, .dataframe td {
#                 text-align: center !important;
#                 min-width: 200px !important;
#             }
#         </style>
#     """

#     # Apply styling to the DataFrame
#     styled_df = ndf.set_index("Symbol").style.set_properties(**{'text-align': 'center'})

#     # Display the custom CSS and the styled DataFrame
#     st.markdown(custom_css, unsafe_allow_html=True)
#     return st.dataframe(styled_df, use_container_width=True)



def display_metrics_charts(metrics_data: list[dict[str, Any]], key_metrics_ttm_data: dict[str, Any]):

    def create_compact_line_chart(data: pl.DataFrame, x_col, y_col, title, ttm_value):
        fig = go.Figure()

        # Historical data line
        fig.add_trace(
            go.Scatter(
                x=data[x_col],
                y=data[y_col],
                mode="lines+markers",
                line=dict(width=2, color="royalblue"),  # Professional blue color
                marker=dict(size=6, color="royalblue", line=dict(width=1, color="darkblue")),
                name=f"Historical",
            )
        )

        # TTM value point
        latest_date = data[x_col].dt.max()
        fig.add_trace(
            go.Scatter(
                x=[latest_date],
                y=[ttm_value],
                mode="markers+text",
                marker=dict(
                    size=6,
                    color="firebrick",
                    symbol="diamond",
                    line=dict(width=2, color="darkred"),
                ),
                name=f"TTM",
                text=[f"{ttm_value:.2f}"],  # Display TTM value as text
                textposition="top center",
            )
        )

        # Horizontal line for TTM value
        fig.add_shape(
            type="line",
            x0=data[x_col].dt.min(),
            y0=ttm_value,
            x1=latest_date,
            y1=ttm_value,
            line=dict(color="firebrick", width=2, dash="dash"),
        )

        # Update layout for a more professional appearance
        fig.update_layout(
            title="",
            title_font=dict(size=16, family="Arial", color="black"),
            xaxis_title="Year",
            yaxis_title=title,
            plot_bgcolor="white",  # Clean background
            height=400,
            margin=dict(l=40, r=40, t=40, b=40),
            font=dict(family="Arial", size=12),
            showlegend=True,
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
            hovermode="x unified",  # Unified hover for better readability
        )

        # Customize axes
        fig.update_xaxes(
            tickmode="array",
            tickvals=data[x_col],
            ticktext=data[x_col],
            gridcolor="lightgrey",
        )
        fig.update_yaxes(gridcolor="lightgrey")

        return fig

    # Create charts
    df = (
        pl.DataFrame(metrics_data)
        .with_columns(
            pl.col("date")
            .str.strptime(pl.Date, format="%Y-%m-%d")
            .alias("FYDateEnding")
        )
        .sort("date")
        .drop("date")
    )

    if df is None:
        print("Dataframe is empty")
        return None



    def plot_chart(metrics: list[tuple[str, str]]):
        for metric, title in metrics:
            ttm_value = key_metrics_ttm_data[f"{metric}_ttm"]
            dfx = df.select("FYDateEnding", f"{metric}")

            st.plotly_chart(
                create_compact_line_chart(
                    dfx,
                    x_col="FYDateEnding",
                    y_col=f"{metric}",
                    title=f"{title}",
                    ttm_value=ttm_value,
                ),
                use_container_width=True,
            )


    col1, col2  = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)

    with col1:
        col1_metrics = [("rev_per_share", "Rev/Share"),]
        plot_chart(col1_metrics)
    with col2:
        col2_metrics = [("pe_ratio", "PE Ratio"),]
        plot_chart(col2_metrics)
    with col3:
        col3_metrics = [("fcf_per_share", "FCF/Share"),]
        plot_chart(col3_metrics)
    with col4:
        col4_metrics = [("ev_over_ebitda", "EV/EBITDA"),]
        plot_chart(col4_metrics)
    with col5:
        col5_metrics = [("ev_to_fcf", "EV/FCF"),]
        plot_chart(col5_metrics)
    with col6:
        col6_metrics = [("fcf_yield", "FCF Yield"),]
        plot_chart(col6_metrics)



def display_growth_charts(growth_data: list[dict[str, Any]]):
    def create_compact_line_chart(data: pl.DataFrame, x_col, y_col, title):
        fig = go.Figure()

        # Historical data line
        fig.add_trace(
            go.Scatter(
                x=data[x_col],
                y=data[y_col],
                mode="lines+markers",
                line=dict(width=2, color="royalblue"),  # Professional blue color
                marker=dict(
                    size=6, color="royalblue", line=dict(width=1, color="darkblue")
                ),
                name="", #f"Historical {title}",
            )
        )

        # Update layout for a more professional appearance
        fig.update_layout(
            title="",
            title_font=dict(size=16, family="Arial", color="black"),
            xaxis_title="Year",
            yaxis_title=title,
            plot_bgcolor="white",  # Clean background
            height=400,
            margin=dict(l=40, r=40, t=40, b=40),
            font=dict(family="Arial", size=12),
            showlegend=True,
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
            hovermode="x unified",  # Unified hover for better readability
        )

        # Customize axes
        fig.update_xaxes(
            tickmode="array",
            tickvals=data[x_col],
            ticktext=data[x_col],
            gridcolor="lightgrey",
        )
        fig.update_yaxes(gridcolor="lightgrey")

        return fig

    # Create charts
    df = (
        pl.DataFrame(growth_data)
        .with_columns(
            pl.col("date")
            .str.strptime(pl.Date, format="%Y-%m-%d")
            .alias("Year")
        )
        .sort("date")
        .drop("date")
    )

    if df is None:
        print("Dataframe is empty")
        return None


    def plot_chart(metrics: list[tuple[str, str]]):
        for metric, title in metrics:
            dfx = df.select("Year", f"{metric}")

            st.plotly_chart(
                create_compact_line_chart(
                    dfx,
                    x_col="Year",
                    y_col=f"{metric}",
                    title=f"{title}",
                ),
                use_container_width=True,
            )

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)

    with col1:
        col1_metrics = [("rev_growth", "Rev Growth"),]
        plot_chart(col1_metrics)
    with col2:
        col2_metrics = [("eps_growth", "EPS Growth"),]
        plot_chart(col2_metrics)
    with col3:
        col3_metrics = [("dps_growth", "DPS Growth"),]
        plot_chart(col3_metrics)
    with col4:
        col4_metrics = [("fcf_growth", "FCF Growth"),]
        plot_chart(col4_metrics)
    with col5:
        col5_metrics = [("debt_growth", "Debt Growth"),]
        plot_chart(col5_metrics)
    # with col6:
    #     col6_metrics = [("fcf_yield", "FCF Yield"),]
    #     plot_chart(col6_metrics)



def main():
    # Main UI
    st.set_page_config(
    page_title="Stock Valuation Dashboard",
    layout="wide",
    )

    st.title("Stock Valuation Dashboard")
    #st.divider()
    st.subheader(
        "Get stock quality and valuation insights from historical financial data.",
        divider="gray",
    )

    st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)

    # Sidebar
    st.sidebar.markdown(
            """
            <style>
            .stTextInput > div > div > input {
                border: 0.5px solid gray;
                border-radius: 8px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
    ticker = st.sidebar.text_input(r"$\textsf{\Large Enter stock symbol:}$")
    analyze_button = st.sidebar.button("Analyze")

    if ticker and analyze_button:
        # Get data
        stock_data = asyncio.run(extract_source_data(ticker))
        profile_data = stock_data["profile"][0]
        quote_data = stock_data["quote"][0]
        ratings_data = stock_data["ratings"]
        key_metrics_ttm_data = stock_data["key_metrics_ttm"][0]
        key_metrics_data = stock_data["key_metrics"]
        growth_data = stock_data["growth"]

        table_data = [quote_data, key_metrics_ttm_data, growth_data, ratings_data,]

        if stock_data:

            # Display ticker profile
            display_profile(profile_data)

            # Display ticker quotes
            #st.markdown("#### Key Metrics")
            display_quotes(quote_data, profile_data)
            # st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
            st.divider()

            display_metric_tables(table_data)

            st.divider()

            # st.markdown("#### Ratings")
            # display_ratings(ratings_data)

            left, right = st.columns(2)

            with left:
                st.markdown("#### Valuation Metrics")
                display_metrics_charts(key_metrics_data, key_metrics_ttm_data)
            with right:
                st.markdown("#### Growth Metrics")
                display_growth_charts(growth_data)



if __name__ == "__main__":
    main()








# analysis = analyze_stock(data)
# st.subheader("Growth Rates")
# for metric, value in analysis.items():
#     st.metric(metric, f"{value:.2%}")

# quality_stock = is_quality_dividend_growth_stock(analysis)
# st.subheader("Quality Dividend Growth Stock")
# st.write("Yes" if quality_stock else "No")

# current_price = st.number_input("Enter current stock price:")
# if current_price:
#     undervalued = is_undervalued(current_price, analysis)
#     st.subheader("Stock Valuation")
#     st.write("Undervalued" if undervalued else "Overvalued")


# /Users/skyfox/dim-dev/dimPythonProject/dim_projects/stock-valuation-app/src/stock_valuation_app/ui/app.py





# Based on the search results, here are the top 6 metrics you can plot on a chart to determine a company valuation, without comparing to other companies:

# 1. Revenue Growth Rate: This metric shows the percentage increase in revenue over time, indicating the company's growth trajectory[1].

# 2. Earnings per Share (EPS): EPS represents the company's profit allocated to each outstanding share of common stock[4].

# 3. Price-to-Earnings (P/E) Ratio: While this typically involves comparison, you can plot the P/E ratio over time to see how the market values the company's earnings[1][4].

# 4. Enterprise Value-to-EBIT (EV/EBIT) Ratio: This metric compares the company's enterprise value to its earnings before interest and taxes, providing insight into the company's value relative to its operating earnings[1].

# 5. Enterprise Value-to-Free Cash Flow (EV/FCF) Ratio: This measures the company's enterprise value relative to its free cash flow, indicating the company's ability to generate excess cash[1].

# 6. Net Revenue Retention (NRR): This metric is particularly important for SaaS companies, showing the percentage of recurring revenue retained from existing customers over time[5].

# These metrics, when plotted over time, can provide valuable insights into a company's financial health, growth potential, and overall valuation. Remember that while these metrics are useful individually, a comprehensive valuation should consider multiple factors and industry-specific nuances.

# Citations:
# [1] https://quartr.com/insights/investing/valuation-metrics-estimating-the-true-worth-of-a-company
# [2] https://www.adamsbrowncpa.com/blog/how-investors-evaluate-key-metrics-in-a-business-valuation/
# [3] https://eqvista.com/business-valuation-metrics/
# [4] https://www.business-case-analysis.com/valuation.html
# [5] https://www.saasacademy.com/blog/saas-company-valuation-metrics
# [6] https://365financialanalyst.com/knowledge-hub/financial-analysis/valuation-ratios/
# [7] https://www.reddit.com/r/SecurityAnalysis/comments/kwrg26/what_metrics_do_you_use_to_analyse_highgrowth/
# [8] https://corporatefinanceinstitute.com/resources/valuation/types-of-valuation-multiples/




# import streamlit as st
# import streamlit.components.v1 as components


# def create_pe_comparison(label, stock_pe, industry_pe):
#     with open("combined_styles.html", "r") as file:
#         html_content = file.read()

#     formatted_html = (
#         html_content.replace("{label}", label)
#         .replace("{stock_pe}", str(stock_pe))
#         .replace("{industry_pe}", str(industry_pe))
#     )
#     components.html(formatted_html, height=150)


# def display_stock_price(label, stock_price):
#     with open("combined_styles.html", "r") as file:
#         html_content = file.read()

#     formatted_html = html_content.replace("{label}", label).replace(
#         "{stock_price}", str(stock_price)
#     )
#     components.html(formatted_html, height=120)


# # Streamlit app
# def main():
#     st.title("Stock Information Display")
#     create_pe_comparison("PE Comparison", 15.6, 18.2)
#     display_stock_price("AAPL", 150.25)


# if __name__ == "__main__":
#     main()


# import streamlit as st
# import plotly.graph_objects as go
# import pandas as pd
# from typing import Any, List, Dict


# def display_growth_charts(growth_data: List[Dict[str, Any]], ttm_value: float):
#     def create_compact_line_chart(data, x_col, y_col, title, ttm_value):
#         fig = go.Figure()

#         # Historical data line
#         fig.add_trace(
#             go.Scatter(
#                 x=data[x_col],
#                 y=data[y_col],
#                 mode="lines+markers",
#                 line=dict(width=2, color="royalblue"),  # Professional blue color
#                 marker=dict(
#                     size=8, color="royalblue", line=dict(width=1, color="darkblue")
#                 ),
#                 name="Historical Net Income Per Share",
#             )
#         )

#         # TTM value point
#         latest_date = data[x_col].iloc[-1]
#         fig.add_trace(
#             go.Scatter(
#                 x=[latest_date],
#                 y=[ttm_value],
#                 mode="markers+text",
#                 marker=dict(
#                     size=12,
#                     color="firebrick",
#                     symbol="diamond",
#                     line=dict(width=2, color="darkred"),
#                 ),
#                 name="TTM Net Income Per Share",
#                 text=[f"{ttm_value:.2f}"],  # Display TTM value as text
#                 textposition="top center",
#             )
#         )

#         # Horizontal line for TTM value
#         fig.add_shape(
#             type="line",
#             x0=data[x_col].iloc[0],
#             y0=ttm_value,
#             x1=latest_date,
#             y1=ttm_value,
#             line=dict(color="firebrick", width=2, dash="dash"),
#         )

#         # Update layout for a more professional appearance
#         fig.update_layout(
#             title=title,
#             title_font=dict(size=16, family="Arial", color="black"),
#             xaxis_title="Year",
#             yaxis_title="Net Income Per Share",
#             plot_bgcolor="white",  # Clean background
#             height=400,
#             margin=dict(l=40, r=40, t=40, b=40),
#             font=dict(family="Arial", size=12),
#             showlegend=True,
#             legend=dict(
#                 orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
#             ),
#             hovermode="x unified",  # Unified hover for better readability
#         )

#         # Customize axes
#         fig.update_xaxes(
#             tickmode="array",
#             tickvals=data[x_col],
#             ticktext=data[x_col],
#             gridcolor="lightgrey",
#         )
#         fig.update_yaxes(gridcolor="lightgrey")

#         return fig

#     # Create and display the chart
#     chart = create_compact_line_chart(
#         data=pd.DataFrame(growth_data),
#         x_col="FYDateEnding",
#         y_col="netIncomePerShare",
#         title="Net Income Per Share Growth",
#         ttm_value=ttm_value,
#     )

#     st.plotly_chart(chart, use_container_width=True)


# # Example usage with container data
# growth_data = [
#     {"FYDateEnding": "2020-12-31", "netIncomePerShare": 3.00},
#     {"FYDateEnding": "2021-12-31", "netIncomePerShare": 4.50},
#     {"FYDateEnding": "2022-12-31", "netIncomePerShare": 5.00},
#     {"FYDateEnding": "2023-12-31", "netIncomePerShare": 6.00},
# ]
# display_growth_charts(growth_data, ttm_value=5.67)




















# import streamlit as st
# import plotly.graph_objects as go
# from typing import Any, List, Dict


# def display_growth_charts(growth_data: List[Dict[str, Any]], ttm_value: float):
#     def create_compact_line_chart(data, x_col, y_col, title, ttm_value):
#         fig = go.Figure()

#         # Historical data line
#         fig.add_trace(
#             go.Scatter(
#                 x=data[x_col],
#                 y=data[y_col],
#                 mode="lines+markers",
#                 line=dict(width=2, color="blue"),
#                 marker=dict(size=8),
#                 name="Historical Net Income Per Share",
#             )
#         )

#         # TTM value point
#         latest_date = data[x_col].iloc[-1]
#         fig.add_trace(
#             go.Scatter(
#                 x=[latest_date],
#                 y=[ttm_value],
#                 mode="markers",
#                 marker=dict(size=12, color="red", symbol="diamond"),
#                 name="TTM Net Income Per Share",
#             )
#         )

#         # Horizontal line for TTM value
#         fig.add_shape(
#             type="line",
#             x0=data[x_col].iloc[0],
#             y0=ttm_value,
#             x1=latest_date,
#             y1=ttm_value,
#             line=dict(color="red", width=1, dash="dash"),
#         )

#         fig.update_layout(
#             title=title,
#             xaxis_title="Year",
#             yaxis_title="Net Income Per Share",
#             plot_bgcolor="lightgrey",
#             height=400,  # Slightly increased height to accommodate legend
#             margin=dict(l=40, r=40, t=40, b=40),
#             font=dict(family="Arial", size=12),
#             showlegend=True,
#             legend=dict(
#                 orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
#             ),
#         )

#         fig.update_xaxes(tickmode="array", tickvals=data[x_col], ticktext=data[x_col])
#         fig.update_yaxes(gridcolor="white", gridwidth=1)

#         # Add annotation for TTM value
#         fig.add_annotation(
#             x=latest_date,
#             y=ttm_value,
#             text=f"TTM: {ttm_value:.2f}",
#             showarrow=True,
#             arrowhead=2,
#             arrowsize=1,
#             arrowwidth=2,
#             arrowcolor="red",
#             ax=40,
#             ay=-40,
#         )

#         return fig

#     # Assuming you have the TTM value available
#     ttm_value = 5.67  # Replace with actual TTM value

#     # Create and display the chart
#     chart = create_compact_line_chart(
#         data=pd.DataFrame(growth_data),
#         x_col="FYDateEnding",
#         y_col="netIncomePerShare",
#         title="Net Income Per Share Growth",
#         ttm_value=ttm_value,
#     )

#     st.plotly_chart(chart, use_container_width=True)


# # Usage
# growth_data = [...]  # Your list of dictionaries with historical data
# display_growth_charts(growth_data, ttm_value=5.67)