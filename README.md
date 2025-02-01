# FlowUnify

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-312/)
[![License](https://img.shields.io/github/license/TheAldersonProject/OpsDataFlow)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Pyright](https://img.shields.io/badge/types-Pyright-brightgreen.svg)](https://github.com/microsoft/pyright)

This project aims to create a centralized hub for managing data platform processes.


## 🚀 Features

- Centralized logging solution for multistep workflows
- Unique execution ID for process tracing
- Comprehensive debugging capabilities
- Business outcome analysis support
- Type-safe implementation with strict typing

## 📦 Install & Configure

### Clone the repository
```bash
    git clone https://github.com/TheAldersonProject/FlowUnify.git
    cd FlowUnify
```

### Use the Makefile options to install dependencies and configure the project
```bash
    make install
```

## 🔧 Usage
Basic usage example:

```python
import telemetry

telemetry.start(**options)
telemetry.event("Here goes the final message")
telemetry.task("My task", "Task message")
telemetry.step("My step under my task", "Step message")
```

## 🛠 Development

### Requirements
* Python >=3.12
* [uv](https://github.com/astral-sh/uv) for dependency management

### This project uses:
* black for code formatting
* ruff for linting
* pyright for static type checking
* pytest for testing
* pre-commit for git hooks

## Project folders
```
FlowUnify/
├── src/     # Source code
├── tests/            # Test files
├── docs/             # Documentation
├── Makefile         # Build automation
└── pyproject.toml   # Project configuration
```

# 📝 License

This project is licensed under the terms specified in LICENSE file.
