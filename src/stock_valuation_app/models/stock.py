from typing import Optional
from pydantic import BaseModel, Field


class CompanyProfile(BaseModel):
    symbol: str
    company_name: str = Field(...,alias="companyName")
    sector: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None


class Rating(BaseModel):
    #symbol: str
    date: str
    rating: str
    score: int = Field(..., alias="ratingScore")
    recommendation: str = Field(..., alias="ratingRecommendation")
    dcf_score: int = Field(..., alias="ratingDetailsDCFScore")
    dcf_rec: str = Field(..., alias="ratingDetailsDCFRecommendation")
    roe_score: int = Field(..., alias="ratingDetailsROEScore")
    roe_rec: str = Field(..., alias="ratingDetailsROERecommendation")
    roa_score: int = Field(..., alias="ratingDetailsROAScore")
    roa_rec: str = Field(..., alias="ratingDetailsROARecommendation")
    de_score: int = Field(..., alias="ratingDetailsDEScore")
    de_rec: str = Field(..., alias="ratingDetailsDERecommendation")
    pe_score: int = Field(..., alias="ratingDetailsPEScore")
    pe_rec: str = Field(..., alias="ratingDetailsPERecommendation")
    pb_score: int = Field(..., alias="ratingDetailsPBScore")
    pb_rec: str = Field(..., alias="ratingDetailsPBRecommendation")


class Ratios(BaseModel):
    #symbol: str
    year: str = Field(..., alias="calendarYear")
    de_ratio: float = Field(..., alias="debtEquityRatio")
    fcf_ps: float = Field(..., alias="freeCashFlowPerShare")
    pb_ratio: float = Field(..., alias="priceToBookRatio")
    ps_ratio: float = Field(..., alias="priceToSalesRatio")
    pe_ratio: float = Field(..., alias="priceEarningsRatio")
    p_fcf_ratio: float = Field(..., alias="priceToFreeCashFlowsRatio")
    peg_ratio: float = Field(..., alias="priceEarningsToGrowthRatio")
    div_yield: int = Field(..., alias="dividendYield")
    curr_ratio: float = Field(..., alias="currentRatio")


class KeyMetrics(BaseModel):
    #symbol: str
    year: str = Field(..., alias="calendarYear")
    rev_per_share: float = Field(..., alias="revenuePerShare")
    net_income_per_share: float = Field(..., alias="netIncomePerShare")
    op_cf_per_share: float = Field(..., alias="operatingCashFlowPerShare")
    fcf_per_share: float = Field(..., alias="freeCashFlowPerShare")
    book_val_per_share: float = Field(..., alias="bookValuePerShare")
    ev_over_ebitda: float = Field(..., alias="enterpriseValueOverEBITDA")
    fcf_yield: float = Field(..., alias="freeCashFlowYield")
    int_coverage: float = Field(..., alias="interestCoverage")
    roic: float


class Growth(BaseModel):
    #symbol: str
    year: str = Field(..., alias="calendarYear")
    rev_growth: float = Field(..., alias="revenueGrowth")
    net_inc_growth: float = Field(..., alias="netIncomeGrowth")
    eps_growth: float = Field(..., alias="epsdilutedGrowth")
    dps_growth: float = Field(..., alias="dividendsperShareGrowth")
    fcf_growth: float = Field(..., alias="freeCashFlowGrowth")
    rev_growth_10y: float = Field(..., alias="tenYRevenueGrowthPerShare")
    rev_growth_5y: float = Field(..., alias="fiveYRevenueGrowthPerShare")
    rev_growth_3y: float = Field(..., alias="threeYRevenueGrowthPerShare")
    net_inc_growth_10y: float = Field(..., alias="tenYNetIncomeGrowthPerShare")
    net_inc_growth_5y: float = Field(..., alias="fiveYNetIncomeGrowthPerShare")
    net_inc_growth_3y: float = Field(..., alias="threeYNetIncomeGrowthPerShare")
    dps_growth_10y: float = Field(..., alias="tenYDividendperShareGrowthPerShare")
    dps_growth_5y: float = Field(..., alias="fiveYDividendperShareGrowthPerShare")
    dps_growth_3y: float = Field(..., alias="threeYDividendperShareGrowthPerShare")
    bvps_growth: float = Field(..., alias="bookValueperShareGrowth")
    debt_growth: float = Field(..., alias="debtGrowth")


class CombinedModel(BaseModel):
    profile: list[CompanyProfile]
    rating: list[Rating]
    key_metrics: list[KeyMetrics]
    ratios: list[Ratios]
    growth: list[Growth]