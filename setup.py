"""Setup for YapLogger."""

import tomllib
from pathlib import Path
from typing import Any

from setuptools import find_packages, setup


def load_pyproject_toml(file_path: Path) -> dict[str, Any]:
    """Load the pyproject.toml file and return its contents as a dictionary."""
    with file_path.open("rb") as f:
        return tomllib.load(f)


def main() -> None:
    """Main method."""
    pyproject = load_pyproject_toml(Path("pyproject.toml"))
    project = pyproject["project"]

    setup(
        name=project["name"],
        version=project["version"],
        author=project["authors"][1]["name"],
        author_email=project["authors"][0]["email"],
        description=project["description"],
        long_description=open("README.md").read(),  # noqa: PTH123, SIM115
        long_description_content_type="text/markdown",
        url="https://github.com/TheAldersonProject/OpsDataFlow",
        packages=find_packages(include=["opsdataflow*"]),
        package_data={
            "": ["LICENSE", "README.md"],
            "typings": ["**/*.pyi"],  # Include all .pyi files in typings
            "yaplogger": ["py.typed"],  # Marker file for PEP 561 compliance
        },
        classifiers=project["classifiers"],
        python_requires=project["requires-python"],
        install_requires=project["dependencies"],
        zip_safe=False,  # Required for type hints to work properly
    )


if __name__ == "__main__":
    main()
