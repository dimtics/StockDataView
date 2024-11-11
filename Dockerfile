FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install uv && uv pip install -e .

COPY src ./src

CMD ["uvicorn", "stock_valuation_app:app", "--host", "0.0.0.0", "--port", "8000"]