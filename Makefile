.PHONY: help setup test run report clean docker-build docker-run lint format

PYTHON := python3
VENV := venv
BIN := $(VENV)/bin
PIP := $(BIN)/pip
PYTEST := $(BIN)/pytest
STREAMLIT := $(BIN)/streamlit
BLACK := $(BIN)/black
ISORT := $(BIN)/isort
FLAKE8 := $(BIN)/flake8
MYPY := $(BIN)/mypy

help:
	@echo "F1Ops Makefile Commands:"
	@echo "  make setup        - Create virtual environment and install dependencies"
	@echo "  make test         - Run tests with coverage"
	@echo "  make run          - Launch Streamlit dashboard"
	@echo "  make report       - Generate HTML report to artifacts/"
	@echo "  make lint         - Run linters (flake8, mypy)"
	@echo "  make format       - Format code with black and isort"
	@echo "  make clean        - Remove build artifacts and cache"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run app in Docker container"

setup:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"
	$(BIN)/pre-commit install

test:
	$(PYTEST)

run:
	$(STREAMLIT) run src/f1ops/app.py

report:
	$(PYTHON) scripts/export_report.py

lint:
	$(FLAKE8) src/ tests/ scripts/
	$(MYPY) src/ tests/ scripts/

format:
	$(BLACK) src/ tests/ scripts/
	$(ISORT) src/ tests/ scripts/

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache/ .mypy_cache/ htmlcov/ .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

docker-build:
	docker-compose build

docker-run:
	docker-compose up
