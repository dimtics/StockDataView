.PHONY: all deps check test docker-build-dev docker-check docker-test docker-check-ci docker-build-prod docker-run docker-push docker-clean

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

# Dev: Build the builder stage image
docker-build-dev:
	docker build --target builder -t stockdataview:dev .

# Dev: Run linting in container
docker-check: docker-build-dev
	docker run --rm -v $(PWD):/app stockdataview:dev uv run ruff check .

# Dev: Run tests in container
docker-test: docker-build-dev
	docker run --rm stockdataview:dev uv run pytest -v

# CI specific target: Build up to the builder stage and run checks/tests
docker-check-ci: docker-build-dev
	- docker run --rm -v $(PWD):/app stockdataview:dev uv run ruff check .
	- docker run --rm -v $(PWD):/app stockdataview:dev uv run pytest -v


# Prod: Build the production stage image
docker-build-prod:
	docker build --target production -t skytics/stockdataview:latest .

# Prod: Run the app locally
docker-run: docker-build-prod
	docker run --rm -e FMP_API_KEY=${FMP_API_KEY} -p 8501:8501 skytics/stockdataview:latest

# Prod: Push to Docker Hub
docker-push: docker-build-prod
	docker push skytics/stockdataview:latest

# Clean up images
docker-clean:
	- docker image rm stockdataview:dev || true
	- docker image rm skytics/stockdataview:latest || true

# All-in-one for local dev
all: check test docker-build-dev
	@echo "All checks passed!"