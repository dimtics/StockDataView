import httpx
from pydantic import BaseModel


class FinancialData(BaseModel):
    revenue: float
    netIncome: float
    freeCashFlow: float
    dividendsPaid: float


class FMPClient:
    def __init__(self, api_key: str):
        self.base_url = "https://financialmodelingprep.com/api/v3"
        self.api_key = api_key

    async def get_financial_data(
        self, symbol: str, limit: int = 10
    ) -> list[FinancialData]:
        url = f"{self.base_url}/income-statement/{symbol}?limit={limit}&apikey={self.api_key}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return [FinancialData(**item) for item in data]
