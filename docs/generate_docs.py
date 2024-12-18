# noqa: INP001
# whoami: mkdocs.yml
"""Documentation generator script for OpsDataFlow project."""

import sys
from pathlib import Path
from typing import Any, Final

import tomli
from loguru import logger
from mkdocs.commands.build import build
from mkdocs.config import load_config  # pyright: ignore [reportUnknownVariableType]

README_TEMPLATE: Final[str] = """
# OpsDataFlow

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-312/)
[![License](https://img.shields.io/github/license/your-username/opsdataflow)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Pyright](https://img.shields.io/badge/types-Pyright-brightgreen.svg)](https://github.com/microsoft/pyright)

{description}

## 🚀 Features

- Centralized logging solution for multi-step workflows
- Unique execution ID for process tracing
- Comprehensive debugging capabilities
- Business outcome analysis support
- Type-safe implementation with strict typing

## 📦 Installation

```bash
pip install opsdataflow
🔧 Usage
Basic usage example:

from opsdataflow import setup_logger

logger = setup_logger()

def your_workflow():
    logger.info("Starting workflow")
    # Your code here
    logger.success("Workflow completed")
🛠 Development
This project uses:
	•	black for code formatting
	•	ruff for linting
	•	pyright for static type checking
	•	pytest for testing
	•	pre-commit for git hooks
To set up the development environment:

# Clone the repository
git clone https://github.com/your-username/opsdataflow.git
cd opsdataflow

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate

# Install dependencies with uv
uv pip install --editable ".[dev]"

# Install pre-commit hooks
pre-commit install
📝 License
This project is licensed under the terms specified in LICENSE file.
"""


def read_pyproject_toml() -> dict[str, Any]:
    """Read and parse pyproject.toml file.

    Returns:
        Dict[str, Any]: The parsed content of pyproject.toml

    Raises:
        FileNotFoundError: If pyproject.toml is not found
        tomli.TOMLDecodeError: If pyproject.toml is invalid
    """
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        msg = "pyproject.toml not found"
        raise FileNotFoundError(msg)

    with open(pyproject_path, "rb") as f:  # noqa: PTH123
        return tomli.load(f)


def generate_readme(config: dict[str, Any]) -> None:
    """Generate README.md file from template and project configuration.

    Args:
        config: Dict[str, Any]: Project configuration from pyproject.toml
    """
    project_info = config.get("project", {})
    description = project_info.get("description", "")

    readme_content = README_TEMPLATE.format(description=description)

    with open("README.md", "w", encoding="utf-8") as f:  # noqa: PTH123
        f.write(readme_content.lstrip())


def setup_mkdocs() -> None:
    """Configure and generate MkDocs documentation."""
    # Create docs directory if it doesn't exist
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)

    # Create basic documentation structure
    api_dir = docs_dir / "api"
    guides_dir = docs_dir / "guides"
    examples_dir = docs_dir / "examples"

    for directory in [api_dir, guides_dir, examples_dir]:
        directory.mkdir(exist_ok=True)

    # Create index.md if it doesn't exist
    index_path = docs_dir / "index.md"
    if not index_path.exists():
        with open(index_path, "w", encoding="utf-8") as f:  # noqa: PTH123
            f.write("# Welcome to OpsDataFlow Documentation\n\n")
            f.write("This is the documentation for the OpsDataFlow project.\n")


def main() -> int:
    """Main function to generate project documentation.

    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    try:
        config = read_pyproject_toml()
        generate_readme(config)
        setup_mkdocs()

        # Build MkDocs documentation
        mkdocs_config = load_config()
        build(mkdocs_config)

        logger.info("Documentation generated successfully!")

    except Exception as e:  # noqa: BLE001
        logger.exception(f"Error generating documentation: {e}", sys.stderr)
        return 1

    else:
        return 0


if __name__ == "main":
    sys.exit(main())
