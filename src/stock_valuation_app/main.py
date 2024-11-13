import os
import yaml
from dotenv import load_dotenv
from stock_valuation_app.data.fmp_client import FMPClient


# Load environment variables from .env file
load_dotenv()


def load_config():
    """Load configuration from a YAML file."""
    with open("config.yml", "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    return config


def get_section_config(section: str):
    """Get configuration for a specific section."""
    match section:
        case "api":
            return load_config().get("api")
        case "valuation":
            return load_config().get("valuation")
        case "dashboard":
            return load_config().get("dashboard")
        case "database":
            return load_config().get("database")
        case "logging":
            return load_config().get("logging")
        case _:
            raise ValueError(f"Invalid section: {section}")


def get_endpoint(url: str) -> str:
    """Get endpoints from the configuration."""
    api_config = get_section_config("api")
    return api_config.get(f"{url}")


def get_base_url() -> str:
    """Get the base URL from the configuration."""
    return get_endpoint("base_url")


def get_api_key() -> str:
    """Get the API key from the .env file."""
    return os.getenv("FMP_API_KEY", "")


def main() -> None:
    """Main function to fetch data from the Financial Modeling Prep API."""
    api_client = FMPClient()
    rating_endpoint = get_endpoint("rating")
    data = api_client.fetch_data(rating_endpoint, "AAPL")
    print(data)


if __name__ == "__main__":
    main()
