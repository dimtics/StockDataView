from typing import Optional
from pydantic import BaseModel, Field


class CompanyProfile(BaseModel):
    symbol: str
    beta: float
    range: str
    company_name: str = Field(..., alias="companyName")
    sector: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None


class Quote(BaseModel):
    symbol: str
    price: float
    change_percent: Optional[float] = Field(..., alias="changesPercentage")
    year_high: float = Field(..., alias="yearHigh")
    year_low: float = Field(..., alias="yearLow")
    market_cap: float = Field(..., alias="marketCap")
    vol_avg: int = Field(..., alias="avgVolume")
    eps: float
    pe: float
    earning_date: str = Field(..., alias="earningsAnnouncement")
    shares_outstanding: int = Field(..., alias="sharesOutstanding")



class Ratings(BaseModel):
    symbol: str
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


class KeyMetricsTTM(BaseModel):
    rev_per_share_ttm: float = Field(..., alias="revenuePerShareTTM")
    net_income_per_share_ttm: float = Field(..., alias="netIncomePerShareTTM")
    fcf_per_share_ttm: float = Field(..., alias="freeCashFlowPerShareTTM")
    pe_ratio_ttm: float = Field(..., alias="peRatioTTM")
    ev_over_ebitda_ttm: float = Field(..., alias="enterpriseValueOverEBITDATTM")
    ev_to_fcf_ttm: float = Field(..., alias="evToFreeCashFlowTTM")
    fcf_yield_ttm: float = Field(..., alias="freeCashFlowYieldTTM")
    pts_ratio_ttm: float = Field(..., alias="priceToSalesRatioTTM")
    ptb_ratio_ttm: float = Field(..., alias="ptbRatioTTM")
    pfcf_ratio_ttm: float = Field(..., alias="pfcfRatioTTM")
    dvd_yield_pct_ttm: float = Field(..., alias="dividendYieldPercentageTTM")
    dvd_per_share_ttm: float = Field(..., alias="dividendPerShareTTM")
    payout_ratio_ttm: float = Field(..., alias="payoutRatioTTM")


class KeyMetrics(BaseModel):
    symbol: str
    date: str
    rev_per_share: float = Field(..., alias="revenuePerShare")
    fcf_per_share: float = Field(..., alias="freeCashFlowPerShare")
    pe_ratio: float = Field(..., alias="peRatio")
    ev_over_ebitda: float = Field(..., alias="enterpriseValueOverEBITDA")
    ev_to_fcf: float = Field(..., alias="evToFreeCashFlow")
    fcf_yield: float = Field(..., alias="freeCashFlowYield")


class Growth(BaseModel):
    symbol: str
    date: str
    rev_growth: float = Field(..., alias="revenueGrowth")
    eps_growth: float = Field(..., alias="epsdilutedGrowth")
    dps_growth: float = Field(..., alias="dividendsperShareGrowth")
    fcf_growth: float = Field(..., alias="freeCashFlowGrowth")
    debt_growth: float = Field(..., alias="debtGrowth")
    fiveY_rev_growth_per_share: float = Field(..., alias="fiveYRevenueGrowthPerShare")
    fiveY_ni_growth_per_share: float = Field(..., alias="fiveYNetIncomeGrowthPerShare")
    fiveY_dps_growth_per_share: float = Field(..., alias="fiveYDividendperShareGrowthPerShare")
    fiveY_opcf_growth_per_share: float = Field(..., alias="fiveYOperatingCFGrowthPerShare")



class CombinedModel(BaseModel):
    profile: list[CompanyProfile]
    quote: list[Quote]
    ratings: list[Ratings]
    key_metrics_ttm: list[KeyMetricsTTM]
    key_metrics: list[KeyMetrics]
    growth: list[Growth]

