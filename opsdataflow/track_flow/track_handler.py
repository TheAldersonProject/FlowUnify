"""Logger handler."""

from datetime import UTC, datetime
from typing import Any

from loguru import logger

from opsdataflow.tools.uuid import generate_uuid4
from opsdataflow.track_flow.constants import Constants
from opsdataflow.track_flow.enums import Handler, LoggerLevel, TrackerLevel
from opsdataflow.track_flow.handler_configuration import HandlerConfiguration


class Track:
    """Handles logging functionality using the Loguru library.

    This class provides a structured way to handle logging, offering functionalities to configure, log messages
    at different levels, and access the logger instance. The TrackerHandler integrates with the Loguru framework
    to customize log formatting, binding contextual data, and efficiently manage logging operations.

    Attributes:
        parameters (dict[str, Any]): Configuration parameters for the logging handler.
        __handler_uuid (str): Identifier for the logging handler instance.
        _logger: Internal reference to the Loguru logger instance.
    """

    def __init__(self, **kwargs: Any) -> None:
        """Logger class init method."""
        self.parameters: dict[str, Any] = HandlerConfiguration(Handler.LOGGER).configure(**kwargs)
        self.__handler_uuid: str = self.parameters[Constants.HANDLER_UUID_KEY]
        self._logger = logger
        self._logger.bind(
            uuid="",
            handler_uuid="",
            handler_type="",
            generated_utc_timestamp="",
        )

        # removes the default handler
        self._logger.remove(0)

    @property
    def reporter(self) -> Any:
        """Returns the Loguru Logger instance."""
        return self._logger

    async def report(self, level: LoggerLevel | TrackerLevel, message: str, **kwargs: Any) -> None:
        """Unique point to apply changes and log."""
        now_utc: str = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        self._logger.log(
            level.name,
            message,
            uuid=generate_uuid4(),
            handler_uuid=self.__handler_uuid,
            handler_type=Handler.LOGGER.name,
            generated_utc_timestamp=now_utc,
            **kwargs,
        )
