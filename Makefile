.PHONY: all deps check test docker-build docker-check docker-test docker-build-prod docker-run docker-tag docker-push docker-clean docker-check-ci

# Dependency management
deps:
    uv sync

# Linting and formatting
check:
    - uv run ruff check . --fix
    - uv run ruff format .

# Testing
test:
    uv run pytest -v

# Dev: Build the dev image (builder stage)
docker-build:
    docker build --target builder -t stockdataview:dev .

# Dev: ruff check
docker-check: docker-build
    docker run --rm -v $(PWD):/app stockdataview:dev ruff check .

# Dev: test
docker-test: docker-build
    docker run --rm stockdataview:dev pytest -v

# Prod: Build the production image (production stage)
docker-build-prod:
    docker build --target production -t skytics/stockdataview:latest .

# Prod: Run the Streamlit app (production image)
docker-run: docker-build-prod
    docker run --rm -e API_KEY=${API_KEY} -p 8501:8501 skytics/stockdataview:latest

# Prod: Tag production image
docker-tag: docker-build-prod
    docker tag skytics/stockdataview skytics/stockdataview:latest

# Prod: Push prod image to Docker Hub
docker-push: docker-tag
    docker push skytics/stockdataview:latest

# Delete images
docker-clean:
    - docker image rm stockdataview:dev || true
    - docker image rm skytics/stockdataview:latest || true

# CI specific target: Build up to the builder stage and run checks/tests
docker-check-ci: docker-build
    docker run --rm -v $(PWD):/app stockdataview:dev uv run ruff check .
    docker run --rm -v $(PWD):/app stockdataview:dev uv run pytest -v

# All-in-one
all: check test docker-build
    @echo "All checks passed!"