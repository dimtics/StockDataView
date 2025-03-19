from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    base_url: str = "https://financialmodelingprep.com/api/v3"
    annual_ratios: str = "ratios"
    annual_financial_growth: str = "financial-growth"
    rating: str = "rating"
    fmp_api_key: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
