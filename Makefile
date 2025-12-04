# Makefile for Semaphore GitHub Action
# Handles venv setup, dependencies, testing, and CI/CD

# Variables
PYTHON := python3
VENV := .venv
VENV_BIN := $(VENV)/bin
PIP := $(VENV_BIN)/pip
PYTEST := $(VENV_BIN)/pytest
PYTHON_VENV := $(VENV_BIN)/python

# Default target
.PHONY: help
help: ## Show this help message
	@echo "Semaphore GitHub Action - Development Makefile"
	@echo "=============================================="
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Environment setup
.PHONY: venv
venv: $(VENV_BIN)/activate ## Create virtual environment

$(VENV_BIN)/activate:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)
	@echo "✅ Virtual environment created in $(VENV)"

.PHONY: install
install: venv ## Install production dependencies
	@echo "Installing production dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "✅ Production dependencies installed"

.PHONY: install-dev
install-dev: venv ## Install development and testing dependencies
	@echo "Installing development dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt
	@echo "✅ Development dependencies installed"

.PHONY: install-all
install-all: install-dev ## Install all dependencies (alias for install-dev)

# Testing targets
.PHONY: test
test: install-dev ## Run all unit tests
	@echo "Running unit tests..."
	$(PYTEST) test_semaphore_action_fixed.py -v

.PHONY: test-basic
test-basic: install-dev ## Run basic tests only
	@echo "Running basic tests..."
	$(PYTEST) test_basic.py -v

.PHONY: test-coverage
test-coverage: install-dev ## Run tests with coverage report
	@echo "Running tests with coverage..."
	$(PYTEST) test_semaphore_action_fixed.py -v --cov=main --cov-report=term-missing --cov-report=html

.PHONY: test-all
test-all: install-dev ## Run all available tests
	@echo "Running all tests..."
	$(PYTEST) test_basic.py test_semaphore_action_fixed.py -v --cov=main --cov-report=term-missing

.PHONY: test-verbose
test-verbose: install-dev ## Run tests with maximum verbosity
	@echo "Running tests with maximum verbosity..."
	$(PYTEST) test_semaphore_action_fixed.py -vvv --tb=long

# Code quality targets
.PHONY: lint
lint: install-dev ## Run code linting
	@echo "Running code quality checks..."
	$(VENV_BIN)/flake8 main.py test_*.py --max-line-length=120 --ignore=E501,W503 || echo "⚠️ Linting issues found"

.PHONY: format
format: install-dev ## Format code with black
	@echo "Formatting code..."
	$(VENV_BIN)/black main.py test_*.py --line-length=120

.PHONY: security
security: install-dev ## Run security checks
	@echo "Running security checks..."
	$(VENV_BIN)/bandit -r main.py || echo "⚠️ Security issues found"
	$(VENV_BIN)/safety check || echo "⚠️ Dependency vulnerabilities found"

# Development targets
.PHONY: dev-setup
dev-setup: install-dev ## Complete development environment setup
	@echo "Setting up development environment..."
	@echo "✅ Development environment ready!"
	@echo ""
	@echo "To activate the virtual environment:"
	@echo "  source $(VENV)/bin/activate"
	@echo ""
	@echo "To run tests:"
	@echo "  make test"

.PHONY: check
check: test lint security ## Run all quality checks (tests + lint + security)
	@echo "✅ All quality checks completed!"

# Live API testing (safe)
.PHONY: test-live
test-live: install-dev ## Run live API demonstration (safe, no real tasks)
	@echo "Running live API demonstration..."
	$(PYTHON_VENV) test_live_api.py

.PHONY: demo
demo: test-live ## Show live API demo (alias for test-live)

# Docker targets (if Dockerfile exists)
.PHONY: docker-build
docker-build: ## Build Docker image
	@echo "Building Docker image..."
	docker build -t semaphore-action .
	@echo "✅ Docker image built: semaphore-action"

.PHONY: docker-test
docker-test: docker-build ## Test in Docker environment
	@echo "Testing in Docker container with required environment variables..."
	@echo "Environment: INPUT_MYINPUT=world (for early return test)"
	docker run --rm \
		-e INPUT_MYINPUT=world \
		-e INPUT_API_KEY=dummy_key_for_test \
		-e INPUT_API_URL=http://dummy.example.com/api \
		-e INPUT_WS_API_URL=ws://dummy.example.com/api \
		-e INPUT_PROJECT_ID=1 \
		-e GITHUB_OUTPUT=/tmp/github_output \
		semaphore-action
	@echo "✅ Docker test completed successfully"

# Cleanup targets
.PHONY: clean
clean: ## Remove build artifacts and cache
	@echo "Cleaning up build artifacts..."
	rm -rf __pycache__/ .pytest_cache/ htmlcov/ .coverage *.xml
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "*~" -delete
	@echo "✅ Cleanup complete"

.PHONY: clean-venv
clean-venv: ## Remove virtual environment
	@echo "Removing virtual environment..."
	rm -rf $(VENV)
	@echo "✅ Virtual environment removed"

.PHONY: clean-all
clean-all: clean clean-venv ## Complete cleanup (artifacts + venv)
	@echo "✅ Complete cleanup finished"

# CI/CD targets
.PHONY: ci-install
ci-install: ## Install dependencies for CI environment
	@echo "Installing dependencies for CI..."
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	@echo "✅ CI dependencies installed"

.PHONY: ci-test
ci-test: ## Run tests in CI environment
	@echo "Running CI tests..."
	pytest test_semaphore_action_fixed.py -v --cov=main --cov-report=xml --cov-report=term

.PHONY: ci-check
ci-check: ci-test ## Full CI check pipeline
	@echo "✅ CI checks completed successfully!"

# Information targets
.PHONY: info
info: ## Show project information
	@echo "Semaphore GitHub Action Project Information"
	@echo "=========================================="
	@echo "Python version: $$($(PYTHON) --version)"
	@echo "Virtual environment: $(VENV)"
	@echo "Main module: main.py"
	@echo "Test files: test_*.py"
	@echo ""
	@echo "Available test commands:"
	@echo "  make test           - Run main tests"
	@echo "  make test-coverage  - Run with coverage"
	@echo "  make test-all       - Run all tests"
	@echo "  make test-live      - Demo with live API"

.PHONY: status
status: ## Show environment status
	@echo "Environment Status:"
	@echo "==================="
	@if [ -d "$(VENV)" ]; then \
		echo "✅ Virtual environment: EXISTS"; \
		echo "Python: $$($(PYTHON_VENV) --version 2>/dev/null || echo 'NOT AVAILABLE')"; \
		echo "Pip: $$($(PIP) --version 2>/dev/null || echo 'NOT AVAILABLE')"; \
		echo "Pytest: $$($(PYTEST) --version 2>/dev/null || echo 'NOT INSTALLED')"; \
	else \
		echo "❌ Virtual environment: NOT FOUND"; \
		echo "Run 'make venv' to create it"; \
	fi
	@echo ""
	@echo "Files:"
	@ls -la main.py test_*.py 2>/dev/null || echo "Some files missing"

# Quick start target
.PHONY: start
start: dev-setup test ## Quick start: setup environment and run tests
	@echo "🚀 Quick start completed!"
	@echo ""
	@echo "Your development environment is ready!"
	@echo "Run 'make help' to see all available commands."

# Validation target for GitHub Actions
.PHONY: validate
validate: ci-check ## Validate for production (used by GitHub Actions)
	@echo "✅ Validation completed - ready for deployment!"

# Default target when just running 'make'
.DEFAULT_GOAL := help
