import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import httpx

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Stock Valuation Dashboard"),
        dcc.Input(id="stock-input", type="text", placeholder="Enter stock symbol"),
        html.Button("Analyze", id="analyze-button"),
        html.Div(id="valuation-output"),
        dcc.Graph(id="growth-chart"),
    ]
)


@app.callback(
    [Output("valuation-output", "children"), Output("growth-chart", "figure")],
    [Input("analyze-button", "n_clicks")],
    [dash.dependencies.State("stock-input", "value")],
)
def update_valuation(n_clicks, symbol):
    if n_clicks is None or not symbol:
        return dash.no_update, dash.no_update

    # Fetch data from our FastAPI endpoint
    response = httpx.get(f"http://localhost:8000/stock/{symbol}")
    data = response.json()

    # Create valuation output
    valuation_output = [
        html.P(
            f"Is quality dividend growth stock: {data['is_quality_dividend_growth_stock']}"
        ),
        html.P(f"Is undervalued: {data['is_undervalued']}"),
    ]

    # Create growth chart
    traces = []
    for metric, rates in data["growth_rates"].items():
        trace = go.Bar(x=list(rates.keys()), y=list(rates.values()), name=metric)
        traces.append(trace)

    layout = go.Layout(title="Growth Rates", barmode="group")
    figure = go.Figure(data=traces, layout=layout)

    return valuation_output, figure


if __name__ == "__main__":
    app.run_server(debug=True)
