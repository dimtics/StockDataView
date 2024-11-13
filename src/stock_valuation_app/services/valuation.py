import polars as pl
from ..data.fmp_client import FinancialData


def calculate_growth_rates(data: list[FinancialData]) -> dict[str, dict[str, float]]:
    df = pl.DataFrame([d.dict() for d in data])

    metrics = ["revenue", "netIncome", "freeCashFlow", "dividendsPaid"]
    periods = [3, 5, 10]

    results = {}
    for metric in metrics:
        metric_results = {}
        for period in periods:
            if len(df) >= period:
                growth_rate = (df[metric][0] / df[metric][period - 1]) ** (
                    1 / period
                ) - 1
                metric_results[f"{period}y"] = growth_rate
        results[metric] = metric_results

    return results


def is_quality_dividend_growth_stock(growth_rates: dict[str, dict[str, float]]) -> bool:
    revenue_growth = growth_rates["revenue"]["5y"]
    dividend_growth = growth_rates["dividendsPaid"]["5y"]
    return revenue_growth > 0.05 and dividend_growth > 0.05


def is_undervalued(
    growth_rates: dict[str, dict[str, float]], current_pe: float
) -> bool:
    earnings_growth = growth_rates["netIncome"]["5y"]
    fair_pe = earnings_growth * 100  # PEG ratio of 1
    return current_pe < fair_pe
