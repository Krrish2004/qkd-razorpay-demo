# QKD-Razorpay Demo - Makefile for Development
# ===========================================
# 
# This Makefile provides convenient commands for managing the project
# with Poetry. All commands assume Poetry is installed on the system.

.PHONY: help install install-dev test lint format check clean run-web run-cli run-demo docker-build docker-run docs

# Default target
help: ## Show this help message
	@echo "QKD-Razorpay Demo - Development Commands"
	@echo "========================================"
	@echo ""
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "For first-time setup, run: make install"

# Installation Commands
install: ## Install all dependencies (production + development)
	@echo "📦 Installing dependencies with Poetry..."
	poetry install

install-prod: ## Install only production dependencies
	@echo "📦 Installing production dependencies only..."
	poetry install --only=main

install-dev: ## Install development dependencies
	@echo "🛠️  Installing development dependencies..."
	poetry install --with=dev

update: ## Update all dependencies
	@echo "🔄 Updating dependencies..."
	poetry update

# Development Commands
dev: install ## Setup development environment
	@echo "🚀 Setting up development environment..."
	poetry run pre-commit install
	@echo "✅ Development environment ready!"

# Testing Commands
test: ## Run all tests
	@echo "🧪 Running tests..."
	poetry run pytest

test-verbose: ## Run tests with verbose output
	@echo "🧪 Running tests (verbose)..."
	poetry run pytest -v

test-coverage: ## Run tests with coverage report
	@echo "🧪 Running tests with coverage..."
	poetry run pytest --cov=. --cov-report=html --cov-report=term

test-integration: ## Run integration tests only
	@echo "🧪 Running integration tests..."
	poetry run pytest -m integration

test-unit: ## Run unit tests only
	@echo "🧪 Running unit tests..."
	poetry run pytest -m unit

test-quantum: ## Run quantum-specific tests
	@echo "🧪 Running quantum tests..."
	poetry run pytest -m quantum

# Code Quality Commands
lint: ## Run linting checks
	@echo "🔍 Running linting checks..."
	poetry run flake8 .
	poetry run mypy .

format: ## Format code with Black and isort
	@echo "🎨 Formatting code..."
	poetry run black .
	poetry run isort .

format-check: ## Check code formatting without making changes
	@echo "🔍 Checking code formatting..."
	poetry run black --check .
	poetry run isort --check-only .

check: ## Run all code quality checks
	@echo "🔍 Running all code quality checks..."
	poetry run black --check .
	poetry run isort --check-only .
	poetry run flake8 .
	poetry run mypy .

security: ## Run security checks
	@echo "🔒 Running security checks..."
	poetry run bandit -r .
	poetry run safety check

pre-commit: ## Run pre-commit hooks on all files
	@echo "🔍 Running pre-commit hooks..."
	poetry run pre-commit run --all-files

# Application Commands
run-web: ## Start the web application
	@echo "🌐 Starting web application..."
	@echo "Access at: http://localhost:5000"
	poetry run python app.py

run-cli: ## Run CLI demo with default parameters
	@echo "💻 Running CLI demo..."
	poetry run python main.py --qubits 500 --error-rate 0.01 --amount 50000

run-demo: ## Run the demo via run.py (CLI mode)
	@echo "🎯 Running demo..."
	poetry run python run.py --cli

run-presentation: ## Start web app in presentation mode
	@echo "🎯 Starting presentation mode..."
	@echo "Access at: http://localhost:5000/presentation"
	poetry run python app.py

# Environment Management
shell: ## Activate Poetry shell
	@echo "🐚 Activating Poetry shell..."
	poetry shell

env-info: ## Show environment information
	@echo "📋 Environment Information:"
	@echo "=========================="
	poetry env info
	@echo ""
	@echo "Installed packages:"
	poetry show --tree



# Documentation Commands
docs: ## Generate documentation
	@echo "📚 Generating documentation..."
	poetry run sphinx-build -b html docs docs/_build

docs-serve: ## Serve documentation locally
	@echo "📚 Serving documentation..."
	cd docs/_build && python -m http.server 8000

# Cleanup Commands
clean: ## Clean up temporary files and caches
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .tox/
	rm -rf dist/
	rm -rf build/

clean-all: clean ## Clean everything including virtual environment
	@echo "🧹 Deep cleaning (removing virtual environment)..."
	poetry env remove --all

# Build and Distribution
build: ## Build the package
	@echo "📦 Building package..."
	poetry build

publish: ## Publish to PyPI (requires authentication)
	@echo "📤 Publishing to PyPI..."
	poetry publish

publish-test: ## Publish to TestPyPI
	@echo "📤 Publishing to TestPyPI..."
	poetry publish --repository testpypi

# Quick Commands for Development
quick-test: ## Quick test run (no coverage)
	poetry run pytest -x --tb=short

quick-start: install ## Quick start for new developers
	@echo "🚀 Quick start complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  make run-web    # Start web application"
	@echo "  make run-cli    # Run CLI demo"
	@echo "  make test       # Run tests"
	@echo "  make format     # Format code"

# Validation Commands
validate: format lint test ## Run full validation pipeline
	@echo "✅ All validation checks passed!"

# Export requirements for compatibility
export-requirements: ## Export requirements.txt for pip users
	@echo "📄 Exporting requirements.txt..."
	poetry export -f requirements.txt --output requirements-poetry.txt --without-hashes
	poetry export -f requirements.txt --output requirements-poetry-dev.txt --with=dev --without-hashes
	@echo "Generated requirements-poetry.txt and requirements-poetry-dev.txt"

# Utility Commands
version: ## Show current version
	@echo "Current version: $(shell poetry version -s)"

version-bump-patch: ## Bump patch version
	poetry version patch

version-bump-minor: ## Bump minor version
	poetry version minor

version-bump-major: ## Bump major version
	poetry version major

# Project Information
info: ## Show project information
	@echo "QKD-Razorpay Demo Project Information"
	@echo "===================================="
	@echo "Version: $(shell poetry version -s)"
	@echo "Python: $(shell poetry run python --version)"
	@echo "Poetry: $(shell poetry --version)"
	@echo ""
	@echo "Key Dependencies:"
	@poetry show qiskit flask torch razorpay 2>/dev/null || echo "Dependencies not installed - run 'make install'" 