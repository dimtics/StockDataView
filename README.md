# StockDataView

StockDataView is a Streamlit application designed to display and visualize stock data fetched from the Financial Modeling Prep (FMP) API. It provides users with bar charts, tables of stock fundamentals, and ratings for a given stock ticker.

## Features

* **Stock Data Visualization:** Presents stock data in clear and interactive bar charts.
* **Fundamental Data Tables:** Displays key stock fundamentals in easy-to-read tables.
* **Stock Ratings:** Shows ratings information for selected stocks.
* **Containerized Application:** Easily deployable via Docker.
* **API Key Input:** Requires users to provide their FMP API key for data retrieval.
* **Automated CI/CD:** Uses GitHub Actions for continuous integration and deployment.
* **Package Management:** Uses `uv` and `pyproject.toml` for dependency management.
* **Makefile Automation:** Includes a Makefile for streamlined development and deployment workflows.

## Prerequisites

* Docker (for running the application)
* An API key from Financial Modeling Prep (FMP)

## Getting Started

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/dimtics/StockDataView.git
    cd StockDataView
    ```

2.  **Build the Docker Image:**

    ```bash
    make docker-build
    ```

3.  **Run the Docker Container:**

    ```bash
    docker run -p 8501:8501 -e FMP_API_KEY=<your-fmp-api-key> skytics/stockdataview
    ```

    Replace `<your-fmp-api-key>` with your actual FMP API key.

4.  **Access the Application:**

    Open your web browser and navigate to `http://localhost:8501`.

5. **Usage**
* Once the app is running, enter a stock ticker (e.g., AAPL) in the Streamlit interface.
* View the displayed bar charts, tables, stock fundamentals, and ratings fetched from the FMP API.

## Development

### Package Management (uv)

* This project uses `uv` for package management. Dependencies are defined in `pyproject.toml`.
* Sync dependencies from `pyproject.toml`.

To install dependencies:

```bash
uv sync
```

## Makefile Commands
The Makefile automates common development tasks:

* `make docker-build`: Builds the Docker image.
* `make docker-check`: Lints code using ruff.
* `make docker-test`: Runs tests.
* `make docker-run`: Runs the Docker container.


## CI/CD (GitHub Actions)

The `.github/workflows/ci-cd.yml` file defines the CI/CD workflow, which:

* Builds the Docker image on push to the `main` branch.
* Pushes the image to Docker Hub.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.