"""Manages loguru single instance."""

from typing import Any

from loguru import logger as loguru_logger

from telemetry.enums import SignalsGroup, SignalsLevel
from tools import singleton


@singleton
class LoggerHandler:
    """Singleton unique class to handle Loguru instance."""

    def __init__(self) -> None:
        """Initializes class and attributes."""
        self._logger = loguru_logger
        self.__setup_signals_event_types()
        self.__setup_signals_event_groups()

    @property
    def logger(self) -> Any:
        """Returns logger instance."""
        return self._logger

    def __add_level_to_logger(
        self, level: SignalsLevel | SignalsGroup, color: str = "<light-white>", icon: str | None = None
    ) -> None:
        """Adds custom level to logger."""
        self.logger.level(name=level.name, no=level.value, color=color, icon=icon)
        self.logger.debug(f"level {level.name} added to logger.")

    def __setup_signals_event_types(self) -> None:
        """Setup signals event types."""
        # Business signal
        self.__add_level_to_logger(level=SignalsLevel.BUSINESS, color="<magenta>", icon="🔍")
        # Dataset signal
        self.__add_level_to_logger(level=SignalsLevel.DATASET, icon="🔍")
        # Data source signal
        self.__add_level_to_logger(level=SignalsLevel.DATA_SOURCE, icon="🔍")
        # Docs signal
        self.__add_level_to_logger(level=SignalsLevel.DOCS, icon="📄")

    def __setup_signals_event_groups(self) -> None:
        """Setup signals event groups."""
        # Process group
        self.__add_level_to_logger(level=SignalsGroup.PROCESS, color="<green>", icon="✨")
        self.__add_level_to_logger(level=SignalsGroup.TASK, color="<yellow>", icon="🗒️")
        self.__add_level_to_logger(level=SignalsGroup.STEP, color="<cyan>", icon="👣️")
