#!/usr/bin/env python3
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
[![License](https://img.shields.io/github/license/TheAldersonProject/{repo_name})](LICENSE)
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

## 📦 Install & Configure

### Clone the repository
```bash
    git clone https://github.com/TheAldersonProject/{repo_name}.git
    cd {repo_name}
```

### Use the Makefile options to install dependencies and configure the project
```bash
    make install
```

## 🔧 Usage
Basic usage example:

```python
from src import telemetry

telemetry.start(**options)
telemetry.event("Here goes the final message")
telemetry.task("My task", "Task message")
telemetry.step("My step under my task", "Step message")
```

## 🛠 Development

### Requirements
* Python {python_version}
* [uv](https://github.com/astral-sh/uv) for dependency management

### This project uses:
* black for code formatting
* ruff for linting
* pyright for static type checking
* pytest for testing
* pre-commit for git hooks

## Project folders
```
{repo_name}/
├── {source_dir}/     # Source code
├── tests/            # Test files
├── docs/             # Documentation
├── Makefile         # Build automation
└── pyproject.toml   # Project configuration
```

# 📝 License

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
    python_version: str = project_info.get("requires-python", "")

    readme_content = README_TEMPLATE.format(
        repo_name="OpsDataFlow", source_dir="src", description=description, python_version=python_version
    )

    with open("README.md", "w", encoding="utf-8") as f:  # noqa: PTH123
        f.write(readme_content.lstrip())


def setup_mkdocs(construct_site: bool = False) -> None:  # noqa: FBT001, FBT002
    """Configure and generate MkDocs documentation.

    Args:
        construct_site (bool): Defines either the helper site will be created or not.
    """
    # Create docs directory if it doesn't exist
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)

    # Create basic documentation structure
    if construct_site:
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

            # Build MkDocs documentation
            mkdocs_config = load_config()
            build(mkdocs_config)


def main() -> int:
    """Main function to generate project documentation.

    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    try:
        logger.info("Generating documentation...")
        config = read_pyproject_toml()
        logger.info(f"Config file: {config}")
        generate_readme(config)
        setup_mkdocs(construct_site=False)

        logger.info("Documentation generated successfully!")

    except Exception as e:  # noqa: BLE001
        logger.exception(f"Error generating documentation: {e}", sys.stderr)
        return 1

    else:
        return 0


# if __name__ == "main":
logger.info("Starting docs generation.")
sys.exit(main())
