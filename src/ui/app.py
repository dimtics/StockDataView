import asyncio
import streamlit as st
from api.fmp_client import FMPClient
# from services.stock_analysis import (
#     analyze_stock,
#     is_quality_dividend_growth_stock,
#     is_undervalued,
# )

async def main():
    #st.title("Stock Valuation App")
    st.title("Stock Valuation Dashboard")
    st.subheader("Get stock quality and valuation insights from historical financial data.", divider="gray")

    #api_key = st.secrets["FMP_API_KEY"]
    symbol = st.text_input("Enter stock symbol:")

    if st.button("Analyze"):
        # Get stock symbol as user input
        if symbol:
            data = await FMPClient().fetch_data(symbol)

            if data:
                analysis = analyze_stock(data)

                st.subheader("Growth Rates")
                for metric, value in analysis.items():
                    st.metric(metric, f"{value:.2%}")

                quality_stock = is_quality_dividend_growth_stock(analysis)
                st.subheader("Quality Dividend Growth Stock")
                st.write("Yes" if quality_stock else "No")

                current_price = st.number_input("Enter current stock price:")
                if current_price:
                    undervalued = is_undervalued(current_price, analysis)
                    st.subheader("Stock Valuation")
                    st.write("Undervalued" if undervalued else "Overvalued")
        else:
            st.warning("Please enter a valid stock symbol")


if __name__ == "__main__":
    asyncio.run(main())