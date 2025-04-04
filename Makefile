.PHONY: all deps check test docker-build docker-check docker-test docker-build-prod docker-run docker-tag docker-push docker-clean

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
	docker build --target builder -t stock-analysis-project:dev .

# Dev: ruff check
docker-check: docker-build
	docker run --rm -v $(PWD):/app stock-analysis-project:dev ruff check .

# Dev: test
docker-test: docker-build
	docker run --rm stock-analysis-project:dev pytest --verbose

# Prod: Build the production image (production stage)
docker-build-prod:
	docker build --target production -t stock-analysis-project:latest .

# Prod: Run the Streamlit app (production image)
docker-run: docker-build-prod
	docker run --rm -e API_KEY=${API_KEY} -v $(PWD)/data:/app/data -p 8501:8501 stock-analysis-project:latest

# Prod: Tag production image
docker-tag: docker-build-prod
	docker tag stock-analysis-project skytics/stock-analysis-project:latest

# Prod: Push prod image to Docker Hub
docker-push: docker-tag
	docker push skytics/stock-analysis-project:latest

# Delete images
docker-clean:
	- docker image rm stock-analysis-project:dev || true
	- docker image rm stock-analysis-project:latest || true

# All-in-one
all: check test docker-build
	@echo "All checks passed!"





