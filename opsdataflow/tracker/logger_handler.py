"""Logger handler."""

import sys
from datetime import UTC, datetime
from typing import Any

from loguru import logger

from opsdataflow.tools.decorators import singleton
from opsdataflow.tools.uuid import generate_uuid4
from opsdataflow.tracker.constants import Constants
from opsdataflow.tracker.enums import Handler, LoggerLevel
from opsdataflow.tracker.handler_configuration import HandlerConfiguration


@singleton
class LoggerHandler:
    """Provides a logging class for application-wide logging functionality.

    The Log class configures the Loguru logger with specified parameters
    and ensures the logger is available for consistent usage throughout
    the application. It initializes logging configuration and provides a
    customized sink for proper formatting and output of log messages.

    Attributes:
    ----------
    configuration : dict[str, Any]
        A dictionary containing the logging parameters for configuration.
    logger : Any
        The Loguru Logger instance used for logging operations.

    Methods:
    -------
    logger
        Returns the Loguru Logger instance.
    configure_sink(**kwargs: Any)
        Configures the sink for Loguru to customize log output.
    """

    def __init__(self, **kwargs: Any) -> None:
        """Logger class init method."""
        self.parameters: dict[str, Any] = HandlerConfiguration(Handler.LOGGER).configure(**kwargs)
        self.__handler_uuid: str = self.parameters[Constants.HANDLER_UUID_KEY]
        self._logger = logger
        self.__configure_sink()

    @property
    def logger(self) -> Any:
        """Returns the Loguru Logger instance."""
        return self

    def __configure_sink(self, **kwargs: Any) -> None:
        """Set the configuration for loguru sink."""
        self._logger = logger.bind(
            uuid="",
            handler_uuid="",
            handler_type="",
            generated_utc_timestamp="",
        )

        # removes the default handler
        self._logger.remove(0)

        # default sink to sys.stdout
        self._logger.add(
            sink=sys.stdout,
            level=LoggerLevel.TRACE.name,
            format=self.parameters[Constants.LOGGER_SINK_FORMAT_KEY],
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

    def _log(self, level: LoggerLevel, message: str, **kwargs: Any) -> None:
        """Unique point to apply changes and log."""
        now_utc: str = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        self._logger.log(
            level.name,
            message,
            **kwargs,
            uuid=generate_uuid4(),
            handler_uuid=self.__handler_uuid,
            generated_utc_timestamp=now_utc,
            handler_type=Handler.LOGGER.name,
        )

    def trace(self, message: str, **kwargs: Any) -> None:
        """Encapsulated trace method with automatic UID inclusion."""
        self._log(LoggerLevel.TRACE, message, **kwargs)

    def debug(self, message: str, **kwargs: Any) -> None:
        """Encapsulated debug method with automatic UID inclusion."""
        self._log(LoggerLevel.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """Encapsulated info method with automatic UID inclusion."""
        self._log(LoggerLevel.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Encapsulated warning method with automatic UID inclusion."""
        self._log(LoggerLevel.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Encapsulated error method with automatic UID inclusion."""
        self._log(LoggerLevel.ERROR, message, **kwargs)

    def critical(self, message: str, exc_info: str | Exception | None = None, **kwargs: Any) -> None:
        """Encapsulated critical method with automatic UID inclusion."""
        self._log(LoggerLevel.CRITICAL, message, exc_info=exc_info, **kwargs)
