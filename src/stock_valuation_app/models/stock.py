from pydantic import BaseModel, Field
from typing import Optional, List


class FinancialData(BaseModel):
    revenue: float
    net_income: float
    free_cash_flow: float
    dividends_paid: float
    date: str


class GrowthRates(BaseModel):
    revenue: dict[str, float]
    net_income: dict[str, float]
    free_cash_flow: dict[str, float]
    dividends_paid: dict[str, float]


class StockValuation(BaseModel):
    symbol: str
    current_price: float
    pe_ratio: float
    dividend_yield: Optional[float] = None
    growth_rates: GrowthRates
    is_quality_dividend_growth_stock: bool
    is_undervalued: bool


class Stock(BaseModel):
    symbol: str
    company_name: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    financial_data: List[FinancialData]
    valuation: Optional[StockValuation] = None

    class Config:
        schema_extra = {
            "example": {
                "symbol": "AAPL",
                "company_name": "Apple Inc.",
                "sector": "Technology",
                "industry": "Consumer Electronics",
                "financial_data": [
                    {
                        "revenue": 365817000000,
                        "net_income": 94680000000,
                        "free_cash_flow": 90215000000,
                        "dividends_paid": 14467000000,
                        "date": "2022-09-30",
                    }
                ],
            }
        }
