"""Manages loguru single instance."""

from typing import Any

from loguru import logger as loguru_logger

from opsdataflow.tools import singleton


@singleton
class LoggerHandler:
    """Singleton unique class to handle Loguru instance."""

    def __init__(self) -> None:
        """Initializes class and attributes."""
        self._logger = loguru_logger

    @property
    def logger(self) -> Any:
        """Returns logger instance."""
        return self._logger
