"""Logger handler."""

import asyncio
import sys
from typing import Any

from opsdataflow.tools.decorators import singleton
from opsdataflow.tools.uuid import generate_uuid4
from opsdataflow.track_flow.constants import Constants
from opsdataflow.track_flow.enums import Handler, LoggerLevel
from opsdataflow.track_flow.handler_configuration import HandlerConfiguration
from opsdataflow.track_flow.track_handler import Track


@singleton
class Logger(Track):
    """Logger handler class for managing logging functionalities.

    This class extends `TrackerHandler` and is used for handling log messages at different levels such as TRACE, DEBUG,
    INFO, WARNING, ERROR, and CRITICAL. It provides encapsulated methods that include additional functionalities
    like automatic UID inclusion. The logging configurations for the sink are set during initialization. The class
    is implemented as a singleton to ensure a single, consistent logging instance throughout the application.
    """

    def __init__(self, **kwargs: Any) -> None:
        """Logger class init method."""
        self.__parameters: dict[str, Any] = HandlerConfiguration(Handler.LOGGER).build(**kwargs)
        super().__init__(
            handler=Handler.LOGGER,
            handler_uuid=self.__parameters.get(Constants.HANDLER_UUID_KEY, generate_uuid4()),
            **kwargs,
        )
        self.__sink_basic_configuration()

    def __sink_basic_configuration(self, **kwargs: Any) -> None:
        """Set the configuration for Reporter sink."""
        # default sink to sys.stdout
        super().reporter.add(
            sink=sys.stdout,
            level=LoggerLevel.TRACE.value,
            format=self.__parameters[Constants.LOGGER_SINK_FORMAT_KEY],
            filter=None,
            colorize=True,
            serialize=False,
            backtrace=True,
            diagnose=True,
            enqueue=False,
            context=None,
            catch=True,
            **kwargs,
        )

    def trace(self, message: str, **kwargs: Any) -> None:
        """Encapsulated trace method with automatic UID inclusion."""
        asyncio.run(super().report(LoggerLevel.TRACE, message, **kwargs))

    def debug(self, message: str, **kwargs: Any) -> None:
        """Encapsulated debug method with automatic UID inclusion."""
        asyncio.run(super().report(LoggerLevel.DEBUG, message, **kwargs))

    def info(self, message: str, **kwargs: Any) -> None:
        """Encapsulated info method with automatic UID inclusion."""
        asyncio.run(super().report(LoggerLevel.INFO, message, **kwargs))

    def warning(self, message: str, **kwargs: Any) -> None:
        """Encapsulated warning method with automatic UID inclusion."""
        asyncio.run(super().report(LoggerLevel.WARNING, message, **kwargs))

    def error(self, message: str, **kwargs: Any) -> None:
        """Encapsulated error method with automatic UID inclusion."""
        asyncio.run(super().report(LoggerLevel.ERROR, message, **kwargs))

    def critical(self, message: str, exc_info: str | Exception | None = None, **kwargs: Any) -> None:
        """Encapsulated critical method with automatic UID inclusion."""
        asyncio.run(super().report(LoggerLevel.CRITICAL, message, exc_info=exc_info, **kwargs))
