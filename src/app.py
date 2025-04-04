from typing import Any

import plotly.graph_objects as go
import polars as pl
import streamlit as st
import streamlit.components.v1 as components

from data_validation import get_validated_stock_data


def display_profile(profile_data: dict[str, Any]) -> None:
    """Displays company profile in sidebar"""
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


def display_quotes(quote_data: dict[str, Any], profile_data: dict[str, Any]) -> None:
    """Displays company quotes in main area"""

    def display_stock_metric(header, value) -> None:
        """Displays quotes in capsule at the top of the page"""

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
        stock_price = f"${quote_data['price']:,.2f}"
        change_price = f"{quote_data['change_percent']:,.2f}%"
        year_low = f"${quote_data['year_low']:,.2f}"
        year_high = f"${quote_data['year_high']:,.2f}"
        market_cap = f"{quote_data['market_cap']/1_000_000_000:.2f}B"
        vol_avg = f"{quote_data['vol_avg']/1_000_000:.2f}M"
        earning_date = quote_data["earning_date"][:10]
        eps = f"{quote_data['eps']:.2f}"
        shares_outstanding = f"{quote_data["shares_outstanding"]/1_000_000_000:.2f}B"

        # Set page top quotes layout
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
            display_stock_metric("EPS", eps)
        with col8:
            display_stock_metric("Shares", shares_outstanding)
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
        return components.html(table_html, height=185)  # 210

    # Get data and generate tables
    quote_data, key_metrics_ttm_data, growth_data, ratings_data = data
    latest_growth_data = growth_data[0]
    latest_ratings_data = ratings_data[0]

    valuation_data = {
        "PE Ratio (TTM)": f"{quote_data['pe']:,.2f}",
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
        "5Y Rev Growth/Share": f"{latest_growth_data['fiveY_rev_growth_per_share'] * 100:,.2f}%",
        "5Y NI Growth/Share": f"{latest_growth_data['fiveY_ni_growth_per_share'] * 100:,.2f}%",
        "5Y Div Growth/Share": f"{latest_growth_data['fiveY_dps_growth_per_share'] * 100:,.2f}%",
        "5Y OCF Growth/Share": f"{latest_growth_data['fiveY_opcf_growth_per_share'] * 100:,.2f}%",
    }

    dividend_data = {
        "Div Yield (TTM)": f"{key_metrics_ttm_data['dvd_yield_pct_ttm']:,.2f}%",
        "Div/Share (TTM)": f"{key_metrics_ttm_data['dvd_per_share_ttm']:,.2f}",
        "Payout Ratio (TTM)": f"{key_metrics_ttm_data['payout_ratio_ttm'] * 100:,.2f}%",
    }

    rating_data = {
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
        container.empty()

    with col2:
        container.markdown(
            display_table(freecashflow_data, "Cash Flow"), unsafe_allow_html=True
        )
        container.empty()

    with col3:
        container.markdown(
            display_table(growth_metric_data, "Growth"), unsafe_allow_html=True
        )
        container.empty()

    with col4:
        container.markdown(
            display_table(dividend_data, "Dividend"), unsafe_allow_html=True
        )
        container.empty()

    with col5:
        container.markdown(display_table(rating_data, "Rating"), unsafe_allow_html=True)
        container.empty()


def display_metrics_charts(
    metrics_data: list[dict[str, Any]], key_metrics_ttm_data: dict[str, Any]
):
    def create_compact_bar_chart(data: pl.DataFrame, x_col, y_col, title, ttm_value):
        fig = go.Figure()

        # Historical data bars
        fig.add_trace(
            go.Bar(
                x=data[x_col],
                y=data[y_col],
                name="Historical",
                marker=dict(
                    color="#4C78A8",  # Modern blue
                    line=dict(width=1.5, color="#2E2E2E"),  # Dark outline
                ),
                width=0.75,
                opacity=0.9,
                hovertemplate="%{x}: %{y:.2f}",
            )
        )

        # TTM value with high-contrast marker
        latest_date = data[x_col].dt.max()
        fig.add_trace(
            go.Scatter(
                x=[latest_date],
                y=[ttm_value],
                mode="markers+text",
                marker=dict(
                    size=14,
                    color="#F28C38",  # Vibrant orange
                    symbol="diamond",
                    line=dict(width=2, color="#D76F1E"),  # Darker orange outline
                ),
                name="TTM",
                text=[f"{ttm_value:.2f}"],
                textposition="top center",
                textfont=dict(
                    size=13, color="#2E2E2E", weight="bold"
                ),  # Dark gray for visibility
                hovertemplate="TTM: %{y:.2f}",
            )
        )

        # TTM reference line
        fig.add_shape(
            type="line",
            x0=data[x_col].dt.min(),
            y0=ttm_value,
            x1=latest_date,
            y1=ttm_value,
            line=dict(
                color="#F28C38",
                width=2,
                dash="dash",
            ),
        )

        # Adaptive layout
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=16, color="#2E2E2E"),  # Darker gray for contrast
                x=0.5,
                xanchor="center",
                y=0.95,
                yanchor="top",
            ),
            xaxis_title="Year",
            yaxis_title=title,
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot
            paper_bgcolor="rgba(0,0,0,0)",  # Transparent paper
            height=450,
            margin=dict(l=60, r=40, t=80, b=60),
            font=dict(
                family="Inter, Arial, sans-serif",
                size=13,
                color="#2E2E2E",  # Dark gray text
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=12),
                bgcolor="rgba(255,255,255,0.8)",  # Light background for legend on white
            ),
            hovermode="x unified",
            transition_duration=500,
        )

        # Enhanced axes
        fig.update_xaxes(
            tickmode="array",
            tickvals=data[x_col],
            ticktext=data[x_col].dt.strftime("%Y"),
            gridcolor="rgba(0,0,0,0.2)",  # Darker gridlines for white background
            linecolor="#666666",
            linewidth=1.5,
            ticks="outside",
            tickfont=dict(size=12),
            title_font=dict(size=14),
            zeroline=False,
        )

        fig.update_yaxes(
            gridcolor="rgba(0,0,0,0.2)",  # Darker gridlines
            linecolor="#666666",
            linewidth=1.5,
            tickfont=dict(size=12),
            title_font=dict(size=14),
            zeroline=False,
            showline=True,
        )

        # Enhanced hover
        fig.update_traces(
            hoverlabel=dict(
                bgcolor="#FFFFFF",  # White hover background
                font_size=12,
                font_color="#2E2E2E",  # Dark gray text
                bordercolor="#666666",
            ),
        )
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

    if df is None or df.is_empty():
        print("Dataframe is empty")
        return None

    def plot_chart(metrics: list[tuple[str, str]]):
        for metric, title in metrics:
            ttm_value = key_metrics_ttm_data[f"{metric}_ttm"]
            dfx = df.select("FYDateEnding", f"{metric}")

            st.plotly_chart(
                create_compact_bar_chart(
                    dfx,
                    x_col="FYDateEnding",
                    y_col=f"{metric}",
                    title=f"{title}",
                    ttm_value=ttm_value,
                ),
                use_container_width=True,
            )

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)

    with col1:
        col1_metrics = [
            ("rev_per_share", "Rev/Share"),
        ]
        plot_chart(col1_metrics)
    with col2:
        col2_metrics = [
            ("pe_ratio", "PE Ratio"),
        ]
        plot_chart(col2_metrics)
    with col3:
        col3_metrics = [
            ("fcf_per_share", "FCF/Share"),
        ]
        plot_chart(col3_metrics)
    with col4:
        col4_metrics = [
            ("ev_over_ebitda", "EV/EBITDA"),
        ]
        plot_chart(col4_metrics)
    with col5:
        col5_metrics = [
            ("ev_to_fcf", "EV/FCF"),
        ]
        plot_chart(col5_metrics)
    with col6:
        col6_metrics = [
            ("fcf_yield", "FCF Yield"),
        ]
        plot_chart(col6_metrics)


def display_growth_charts(growth_data: list[dict[str, Any]]):
    def create_compact_bar_chart(data: pl.DataFrame, x_col, y_col, title):
        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=data[x_col],
                y=data[y_col],
                name="",
                marker=dict(
                    color="#54A24B",  # Modern green
                    line=dict(width=1.5, color="#2E2E2E"),  # Dark outline
                ),
                width=0.7,
                hovertemplate="%{x}: %{y:.2f}%",
            )
        )

        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=18, color="#2E2E2E"),  # Darker gray
                x=0.5,
                xanchor="center",
                y=0.95,
                yanchor="top",
            ),
            xaxis_title="Year",
            yaxis_title="Growth Rate (%)",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=450,
            margin=dict(l=50, r=50, t=80, b=60),
            font=dict(
                family="Inter, Arial, sans-serif",
                size=13,
                color="#2E2E2E",  # Dark gray text
            ),
            showlegend=False,
            hovermode="x unified",
            barmode="group",
            transition_duration=400,
        )

        fig.update_xaxes(
            tickmode="array",
            tickvals=data[x_col],
            ticktext=data[x_col].dt.strftime("%Y"),
            gridcolor="rgba(0,0,0,0.2)",  # Darker gridlines
            linecolor="#666666",
            linewidth=1,
            ticks="outside",
            tickfont=dict(size=12),
            title_font=dict(size=14),
            zeroline=False,
        )

        fig.update_yaxes(
            gridcolor="rgba(0,0,0,0.2)",
            linecolor="#666666",
            linewidth=1,
            ticksuffix="%",
            tickfont=dict(size=12),
            title_font=dict(size=14),
            zeroline=False,
            showline=True,
        )

        fig.update_traces(
            opacity=0.95,
            hoverlabel=dict(
                bgcolor="#FFFFFF",
                font_size=12,
                font_color="#2E2E2E",
                bordercolor="#666666",
            ),
        )

        return fig

    # Create charts
    df = (
        pl.DataFrame(growth_data)
        .with_columns(
            pl.exclude(["symbol", "date"]).map_elements(
                lambda x: round(x * 100, 2), return_dtype=pl.Float64
            ),
            pl.col("date").str.strptime(pl.Date, format="%Y-%m-%d").alias("Year"),
        )
        .sort("date")
        .drop("date")
    )

    if df is None or df.is_empty():
        print("Dataframe is empty")
        return None

    def plot_chart(metrics: list[tuple[str, str]]):
        for metric, title in metrics:
            dfx = df.select("Year", f"{metric}")

            st.plotly_chart(
                create_compact_bar_chart(
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
        col1_metrics = [
            ("rev_growth", "Rev Growth"),
        ]
        plot_chart(col1_metrics)
    with col2:
        col2_metrics = [
            ("eps_growth", "EPS Growth"),
        ]
        plot_chart(col2_metrics)
    with col3:
        col3_metrics = [
            ("dps_growth", "DPS Growth"),
        ]
        plot_chart(col3_metrics)
    with col4:
        col4_metrics = [
            ("fcf_growth", "FCF Growth"),
        ]
        plot_chart(col4_metrics)
    with col5:
        col5_metrics = [
            ("debt_growth", "Debt Growth"),
        ]
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

    # Custom CSS
    st.markdown(
        """
    <style>
    .custom-divider {
        margin-top: 5px;  /* Adjust this value to control space above */
        margin-bottom: 5px;  /* Adjust this value to control space below */
        border: none;
        border-top: 1px solid rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

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

    st.title("StockDataView")
    # st.divider()
    st.subheader(
        "Visualize stock fundamentals, ratings, and historical data using the Financial Modeling Prep (FMP) API",
        divider="gray",
    )

    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)

    # Sidebar
    ticker = st.sidebar.text_input(r"$\textsf{\Large Enter stock symbol:}$")
    analyze_button = st.sidebar.button("Analyze")

    if ticker and analyze_button:
        # Get data
        stock_data = get_validated_stock_data(ticker)
        profile_data = stock_data["profile"][0]
        quote_data = stock_data["quote"][0]
        ratings_data = stock_data["ratings"]
        key_metrics_ttm_data = stock_data["key_metrics_ttm"][0]
        key_metrics_data = stock_data["key_metrics"]
        growth_data = stock_data["growth"]

        table_data = [
            quote_data,
            key_metrics_ttm_data,
            growth_data,
            ratings_data,
        ]

        if stock_data:
            # Display ticker profile
            display_profile(profile_data)

            # Display ticker quotes
            # st.markdown("#### Key Metrics")
            display_quotes(quote_data, profile_data)
            st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
            st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

            display_metric_tables(table_data)

            st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
            st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)

            left, right = st.columns(2)
            with left:
                st.markdown(
                    """<h4 style="text-align: center;">Valuation Metrics</h4>""",
                    unsafe_allow_html=True,
                )
                display_metrics_charts(key_metrics_data, key_metrics_ttm_data)
            with right:
                st.markdown(
                    """<h4 style="text-align: center;">Growth Metrics</h4>""",
                    unsafe_allow_html=True,
                )
                display_growth_charts(growth_data)

            st.divider()


if __name__ == "__main__":
    main()
