# ./Makefile

# PYTHON
PYTHON_VERSION := $(shell cat .python-version)
PIP = python$(PYTHON_VERSION) -m pip
UV_PY_INSTALL_VERSION = $(PYTHON_VERSION)
UV_PY_VERSION = --python $(UV_PY_INSTALL_VERSION)
UV_ENV_ARGS = --allow-existing

# BLACK
BLACK_ARGS = --config ./pyproject.toml

# RUFF
RUFF = ruff --config ./pyproject.toml
RUFF_ARGS = --target-version py$(PYTHON_VERSION) -n

# PYRIGHT
PYRIGHT = pyright
PYRIGHT_LINT_ARGS = --project pyproject.toml --pythonversion $(UV_PY_INSTALL_VERSION) --stats

# PROJECT
SOURCE_DIR = ./yaplogger
SOURCE_PY_FILES = $(SOURCE_DIR)/**/*.py

TEST_DIR = ./tests
TEST_PY_FILES = $(TEST_DIR)/*.py

# Phony targets
.PHONY: help install format lint test clean build

# Default target
help:
	@echo "Available commands:"
	@echo "  make install    : Install dependencies"
	@echo "  make format     : Format code using Black and isort"
	@echo "  make lint       : Run linters"
	@echo "  make test       : Run tests"
	@echo "  make clean      : Remove build artifacts"
	@echo "  make build      : Runs all above to deploy"

# Install dependencies
install:
	rm -rf .venv
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt
	uv python install $(UV_PY_INSTALL_VERSION)
	uv venv $(UV_PY_VERSION) $(UV_ENV_ARGS)
	uv sync
	uv run pre-commit install

# Format code
format:
	uv run black $(SOURCE_DIR) $(BLACK_ARGS)
	uv run $(RUFF) format $(SOURCE_DIR) $(RUFF_ARGS)

# Lint code
lint:
	uv run black --check $(SOURCE_DIR) $(BLACK_ARGS)
	uv run $(RUFF) check $(SOURCE_DIR) $(RUFF_ARGS) --fix
	uv run $(PYRIGHT) $(SOURCE_DIR) $(PYRIGHT_LINT_ARGS)

# Run tests
test:
	uv run python3 -m pytest $(TEST_DIR)

# Clean build artifacts
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache

# Run the phony as below
build:
	@echo "Clean project files"
	make clean

	@echo "Format project files"
	make format

	@echo "Check project lint"
	make lint

	@echo "Run tests"
	make test

	@echo "Building wheel"
	uv pip install .
