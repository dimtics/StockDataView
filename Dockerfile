# ------------------------------- Builder Satge -------------------------------

# Build stage (with dev tools for linting, testing, etc.)
FROM python:3.12-slim-bookworm AS builder

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Download the latest installer, install it, and remove it
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN chmod -R 655 /uv-installer.sh && /uv-installer.sh && rm /uv-installer.sh

# Set up uv environment PATH
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

# Prevent Python from writing pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy dependency files first for caching
COPY pyproject.toml /app/

# Sync dependencies (includes streamlit, ruff, pytest if in pyproject.toml)
RUN uv sync

# Copy the rest of the project
COPY . /app


# ------------------------- Production Stage -------------------------

# Final stage (production, lean image)
FROM python:3.12-slim-bookworm AS production
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
CMD ["streamlit", "run", "src/app.py"]