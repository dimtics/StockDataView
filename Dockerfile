# Build stage (with dev tools for linting, testing, etc.)
FROM python:3.11-slim AS builder
WORKDIR /app

# Prevent Python from writing pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files first for caching
COPY pyproject.toml uv.lock /app/

# Sync dependencies (includes streamlit, ruff, pytest if in pyproject.toml)
RUN uv sync --frozen

# Copy the rest of the project
COPY . /app

# Final stage (production, lean image)
FROM python:3.11-slim AS production
WORKDIR /app

# Prevent Python from writing pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create a non-privileged user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Copy the virtual env and project files
COPY --from=builder /app/.venv /app/.venv
COPY . /app

# Set PATH to use the virtual env
ENV PATH="/app/.venv/bin:$PATH"

# Switch to non-privileged user
USER appuser

# Expose Streamlit's default port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "app.py"]