import streamlit as st


def display_stock_price(label, stock_price):
    html_content = f"""
    <style>
.stock-box {{
    background-color: #f0f0f0;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    padding: 10px;
    margin-bottom: 10px;
    width: 180px;
    border: 1px solid #e0e0e0;
    text-align: center;
}}
.stock-label {{
    font-weight: bold;
    font-size: 16px;
    color: #2c3e50;
    margin-bottom: 10px;
}}
.price-header {{
    font-size: 12px;
    color: #7f8c8d;
    margin-bottom: 5px;
    font-weight: 300;
}}
.price-value {{
    font-size: 24px;
    font-weight: bold;
    color: #2ecc71;
}}
</style>
<div class="stock-box">
    <div class="stock-label">{label}</div>
    <div class="price-header">Stock Price</div>
    <div class="price-value">${stock_price}</div>
</div>
    """
    st.html(html_content)


# Streamlit app
def main():
    st.title("Stock Price Display")
    display_stock_price("AAPL", 150.25)


if __name__ == "__main__":
    main()
