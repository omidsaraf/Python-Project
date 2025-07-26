# Makefile for Data Pipeline Project

PYTHON = python3
PIP = pip
SRC_DIR = src
TEST_DIR = tests

# Default target
.DEFAULT_GOAL := help

## ----------- Commands -----------

.PHONY: help
help: ## Show help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "🔧 \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	$(PIP) install -r requirements.txt

format: ## Format code using black and isort
	black $(SRC_DIR) $(TEST_DIR)
	isort $(SRC_DIR) $(TEST_DIR)

lint: ## Run flake8 for linting
	flake8 $(SRC_DIR) $(TEST_DIR)

typecheck: ## Run mypy for static type checking
	mypy $(SRC_DIR) $(TEST_DIR)

test: ## Run tests using pytest
	pytest --maxfail=3 --disable-warnings -q

check: format lint typecheck test ## Run full code quality checks

docker-build: ## Build docker image
	docker build -t data-pipeline .

run: ## Run the pipeline
	$(PYTHON) run_pipeline.py --config configs/pipeline_config.yaml
