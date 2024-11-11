# Stock Valuation Dashboard

## Overview

This project is a web-based stock valuation dashboard that helps investors analyze dividend growth stocks. It provides insights into stock quality and valuation based on historical financial data.

Key features:
- Fetches financial data from Financial Modeling Prep API
- Calculates growth rates for revenue, dividends, cash flow, and other metrics
- Determines if a stock is a quality dividend growth stock
- Assesses whether a stock is undervalued or reasonably valued
- Visualizes key metrics and growth rates

## Tech Stack

- Python 3.11+
- FastAPI: Web framework for building APIs
- Dash: React-based framework for building analytical web applications
- Polars: Fast DataFrame library for data manipulation
- Pydantic: Data validation using Python type annotations
- PyArrow: Efficient data interchange format
- DuckDB: Embedded analytical database
- uv: Python packaging and dependency management tool
- Docker: Containerization
- GitHub Actions: CI/CD pipeline

## Project Structure

stock_valuation_app/
├── .github/workflows/ # CI/CD configuration
├── src/
│ └── stock_valuation_app/
│ ├── api/ # FastAPI routes
│ ├── data/ # Data fetching and processing
│ ├── models/ # Pydantic models
│ ├── services/ # Business logic
│ └── ui/ # Dash dashboard
├── tests/ # Unit and integration tests
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml # Project metadata and dependencies
├── README.md
└── uv.lock # Dependency lock file



## Setup and Installation

1. Clone the repository:
git clone https://github.com/dimtics/stock_valuation_app.git
cd stock_valuation_app

2. Install uv and project dependencies:
pip install uv
uv pip install -e .

3. Set up environment variables:
Create a `.env` file in the project root and add your Financial Modeling Prep API key:
FMP_API_KEY=your_api_key_here

4. Run the application:
uvicorn stock_valuation_app:app --reload

5. Open your browser and navigate to `http://localhost:8000/dashboard` to view the dashboard.


## Docker Deployment

To run the application using Docker:

1. Build the Docker image:
docker build -t stock-valuation-app .
docker run -p 8000:8000 -e FMP_API_KEY=your_api_key_here stock-valuation-app

Alternatively, use Docker Compose:
docker-compose up



## Usage

1. Enter a stock symbol in the input field on the dashboard.
2. Click the "Analyze" button to fetch and analyze the stock data.
3. View the growth rates, quality assessment, and valuation results.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.