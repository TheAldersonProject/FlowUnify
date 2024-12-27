# Environment variables
SHELL := /bin/bash
.DEFAULT_GOAL := help

define format_py_version
$(shell echo "py$(subst .,,$(1))")
endef

# PYTHON
PYTHON_VERSION := $(shell cat .python-version)
PIP = python$(PYTHON_VERSION) -m pip
UV_PY_INSTALL_VERSION = $(PYTHON_VERSION)
UV_PY_VERSION = --python $(UV_PY_INSTALL_VERSION)
UV_ENV_ARGS = --allow-existing

# PROJECT
SOURCE_DIR = ./opsdataflow
TEST_DIR = ./tests
DOCS_DIR = ./docs
CONFIG_FILE = pyproject.toml

# TOOLS
BLACK_ARGS = --config $(CONFIG_FILE)
RUFF = ruff --config $(CONFIG_FILE)
#RUFF_ARGS = --target-version py312 -n
RUFF_ARGS = --target-version $(call format_py_version,$(UV_PY_INSTALL_VERSION)) -n
PYRIGHT = pyright
PYRIGHT_ARGS = --project $(CONFIG_FILE) --pythonversion $(UV_PY_INSTALL_VERSION) --stats
PYTEST_ARGS = --cov=$(SOURCE_DIR) --cov-report=xml --cov-report=term-missing

# Colors for terminal output
BLUE := \033[0;34m
NC := \033[0m # No Color
INFO := @echo "[INFO]"

.PHONY: help install dev-install format lint test clean build version check docs

help:
	@echo "🚀 OpsDataFlow Development Commands"
	@echo ""
	@echo "Development:"
	@echo "  make install      : Clean install of dependencies"
	@echo "  make dev-install  : Install development dependencies"
	@echo "  make format       : Format code using Black and Ruff"
	@echo "  make lint         : Run all linters"
	@echo "  make test         : Run tests with coverage"
	@echo "  make check        : Run format, lint, and test"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs         : Generate documentation"
	@echo ""
	@echo "Deployment:"
	@echo "  make clean        : Remove build artifacts"
	@echo "  make version      : Update version and changelog"
	@echo "  make build        : Build package"

install:
	${INFO} "Installing dependencies..."
	rm -rf .venv
	python3 -m pip install --upgrade pip
	python3 -m pip install uv
	uv python install $(UV_PY_INSTALL_VERSION)
	uv venv $(UV_PY_VERSION) $(UV_ENV_ARGS)
	uv run python -m ensurepip --upgrade
	uv sync

dev-install: install
	${INFO} "Installing development dependencies..."
	uv run pre-commit install
	uv pip install -e ".[dev]"

format:
	${INFO} "Formatting code..."
	uv run black $(SOURCE_DIR) $(TEST_DIR) $(BLACK_ARGS)
	uv run $(RUFF) format $(SOURCE_DIR) $(TEST_DIR) $(RUFF_ARGS)

lint:
	${INFO} "Linting code..."
	uv run black --check $(SOURCE_DIR) $(TEST_DIR) $(BLACK_ARGS)
	uv run $(RUFF) check $(SOURCE_DIR) $(TEST_DIR) $(RUFF_ARGS) --fix
	uv run $(PYRIGHT) $(SOURCE_DIR) $(PYRIGHT_ARGS)

test:
	${INFO} "Running tests..."
	uv run pytest $(TEST_DIR) $(PYTEST_ARGS)

check: format lint test

clean:
	${INFO} "Cleaning project..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache build dist *.egg-info .coverage coverage.xml

docs:
	${INFO} "Generating documentation..."
	uv run mkdocs build --strict
	uv run python ./docs/generate_docs.py

version: check
	${INFO} "Updating version and changelog..."
	uv run git-changelog --config-file $(CONFIG_FILE) -o CHANGELOG.md

build: check
	${INFO} "Building package..."
	uv pip install build
	uv run python -m build
