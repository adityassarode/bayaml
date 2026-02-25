# =====================================
# Baya - ML Orchestration Framework
# =====================================

PYTHON=python
PIP=pip
PACKAGE=baya

.DEFAULT_GOAL := help

help:
	@echo "Available commands:"
	@echo "  make install        Install package in editable mode"
	@echo "  make dev            Install dev dependencies"
	@echo "  make format         Format code with black"
	@echo "  make lint           Run linter (ruff)"
	@echo "  make typecheck      Run type checking (mypy)"
	@echo "  make test           Run tests"
	@echo "  make coverage       Run tests with coverage"
	@echo "  make build          Build package"
	@echo "  make publish-test   Publish to TestPyPI"
	@echo "  make publish        Publish to PyPI"
	@echo "  make clean          Clean build files"
	@echo "  make docs           Build documentation"
	@echo "  make run            Run CLI"
	@echo "  make precommit      Run all checks"

# =========================
# Installation
# =========================

install:
	$(PIP) install -e .

dev:
	$(PIP) install -e .
	$(PIP) install -r requirements-dev.txt

# =========================
# Formatting & Linting
# =========================

format:
	black .
	ruff check . --fix

lint:
	ruff check .

typecheck:
	mypy $(PACKAGE)

# =========================
# Testing
# =========================

test:
	pytest

coverage:
	pytest --cov=$(PACKAGE) --cov-report=term --cov-report=html

# =========================
# Build & Publish
# =========================

build:
	rm -rf dist build *.egg-info
	$(PYTHON) -m build

publish-test:
	$(PYTHON) -m twine upload --repository testpypi dist/*

publish:
	$(PYTHON) -m twine upload dist/*

# =========================
# Documentation
# =========================

docs:
	cd docs && make html

# =========================
# CLI
# =========================

run:
	$(PYTHON) -m baya

# =========================
# Cleanup
# =========================

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	find . -type d -name "__pycache__" -exec rm -r {} +

# =========================
# Full Pre-Commit Check
# =========================

precommit:
	make format
	make lint
	make typecheck
	make test
