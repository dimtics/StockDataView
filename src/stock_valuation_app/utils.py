from pathlib import Path

import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def load_config():
    """Load configuration from a YAML file."""
    with open(Path("src/config.yml").absolute(), "r", encoding="utf-8") as file:
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
