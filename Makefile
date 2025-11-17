.PHONY: help install install-dev clean lint format type-check test test-cov run-app run-cli build docker-build docker-run pre-commit setup

.DEFAULT_GOAL := help

# Color output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Display this help message
	@echo "$(BLUE)Factory Feature - Makefile Commands$(NC)"
	@echo "$(GREEN)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@awk 'BEGIN {FS = ":.*##"; printf "\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  $(YELLOW)%-18s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(BLUE)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
	@echo ""

##@ Installation

install: ## Install production dependencies using uv
	@echo "$(GREEN)Installing production dependencies with uv...$(NC)"
	uv pip install -e .

install-dev: ## Install all dependencies including dev tools
	@echo "$(GREEN)Installing all dependencies (including dev) with uv...$(NC)"
	uv pip install -e ".[dev]"
	@echo "$(GREEN)Installing pre-commit hooks...$(NC)"
	pre-commit install

setup: install-dev ## Complete development environment setup
	@echo "$(GREEN)Setting up development environment...$(NC)"
	@echo "$(YELLOW)Creating .env file from template if it doesn't exist...$(NC)"
	@test -f .env || cp .env.example .env
	@echo "$(GREEN)Setup complete! Edit .env file with your credentials.$(NC)"

##@ Code Quality

lint: ## Run linting with ruff
	@echo "$(GREEN)Running ruff linter...$(NC)"
	ruff check src/ tests/ app.py main.py content.py

format: ## Format code with black and ruff
	@echo "$(GREEN)Formatting code with black...$(NC)"
	black src/ tests/ app.py main.py content.py
	@echo "$(GREEN)Sorting imports with ruff...$(NC)"
	ruff check --select I --fix src/ tests/ app.py main.py content.py

type-check: ## Run type checking with mypy
	@echo "$(GREEN)Running mypy type checker...$(NC)"
	mypy src/ --ignore-missing-imports

pre-commit: ## Run pre-commit hooks on all files
	@echo "$(GREEN)Running pre-commit hooks...$(NC)"
	pre-commit run --all-files

quality: lint type-check ## Run all code quality checks
	@echo "$(GREEN)All code quality checks passed!$(NC)"

##@ Testing

test: ## Run tests with pytest
	@echo "$(GREEN)Running tests...$(NC)"
	pytest tests/ -v

test-cov: ## Run tests with coverage report
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html

test-fast: ## Run tests excluding slow tests
	@echo "$(GREEN)Running fast tests only...$(NC)"
	pytest tests/ -v -m "not slow"

##@ Running Application

run-app: ## Run the Gradio web application
	@echo "$(GREEN)Starting Gradio web application...$(NC)"
	@test -f .env || (echo "$(RED)Error: .env file not found. Run 'make setup' first.$(NC)" && exit 1)
	python app.py

run-cli: ## Run CLI with example prompt (use PROMPT="your text" to customize)
	@echo "$(GREEN)Running Factory Feature CLI...$(NC)"
	@test -f .env || (echo "$(RED)Error: .env file not found. Run 'make setup' first.$(NC)" && exit 1)
	python main.py --prompt "$(or $(PROMPT),Add logging functionality to all major modules in the project)"

##@ Cleaning

clean: ## Remove build artifacts, cache, and generated files
	@echo "$(GREEN)Cleaning build artifacts and cache...$(NC)"
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .eggs/
	@echo "$(GREEN)Cleanup complete!$(NC)"

clean-all: clean ## Remove all generated files including projects and databases
	@echo "$(YELLOW)Removing generated projects and databases...$(NC)"
	rm -rf project_new/
	rm -rf chroma_db/
	rm -f project_new.zip
	rm -f factory_feature.log
	@echo "$(GREEN)Deep cleanup complete!$(NC)"

##@ Building & Distribution

build: clean ## Build distribution packages
	@echo "$(GREEN)Building distribution packages...$(NC)"
	uv build

publish-test: build ## Publish to TestPyPI
	@echo "$(GREEN)Publishing to TestPyPI...$(NC)"
	uv publish --repository testpypi

publish: build ## Publish to PyPI
	@echo "$(YELLOW)Publishing to PyPI...$(NC)"
	@read -p "Are you sure you want to publish to PyPI? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		uv publish; \
	else \
		echo "$(RED)Publication cancelled.$(NC)"; \
	fi

##@ Docker

docker-build: ## Build Docker image
	@echo "$(GREEN)Building Docker image...$(NC)"
	docker build -t factory-feature:latest .

docker-run: ## Run Docker container
	@echo "$(GREEN)Running Docker container...$(NC)"
	docker run -p 7860:7860 --env-file .env factory-feature:latest

##@ Development

dev: ## Start development environment with auto-reload
	@echo "$(GREEN)Starting development mode...$(NC)"
	watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- python app.py

notebook: ## Start Jupyter notebook server
	@echo "$(GREEN)Starting Jupyter notebook...$(NC)"
	jupyter notebook

##@ Information

info: ## Display project information
	@echo "$(BLUE)Project Information$(NC)"
	@echo "$(GREEN)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo "Project: Factory Feature"
	@echo "Version: 1.0.0"
	@echo "Author: Ruslan Magana"
	@echo "Website: https://ruslanmv.com"
	@echo "License: Apache-2.0"
	@echo "Python: $$(python --version)"
	@echo "$(GREEN)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"

##@ Utility

env-check: ## Check if required environment variables are set
	@echo "$(GREEN)Checking environment variables...$(NC)"
	@test -f .env && echo "$(GREEN)✓ .env file exists$(NC)" || echo "$(RED)✗ .env file missing$(NC)"
	@test -n "$$WATSONX_APIKEY" && echo "$(GREEN)✓ WATSONX_APIKEY is set$(NC)" || echo "$(YELLOW)⚠ WATSONX_APIKEY not set$(NC)"
	@test -n "$$PROJECT_ID" && echo "$(GREEN)✓ PROJECT_ID is set$(NC)" || echo "$(YELLOW)⚠ PROJECT_ID not set$(NC)"

tree: ## Display project tree structure
	@echo "$(GREEN)Project Structure:$(NC)"
	@tree -I '__pycache__|*.pyc|.git|.venv|chroma_db|project_old|project_new|backup' -L 3

verify: quality test ## Run all verification checks (lint, type-check, tests)
	@echo "$(GREEN)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo "$(GREEN)✓ All verification checks passed!$(NC)"
	@echo "$(GREEN)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
