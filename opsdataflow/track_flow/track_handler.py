"""Logger handler."""

from datetime import UTC, datetime
from typing import Any

from loguru import logger

from opsdataflow.tools.uuid import generate_uuid4
from opsdataflow.track_flow.constants import Constants
from opsdataflow.track_flow.enums import Handler, LoggerLevel, TrackerGroup, TrackerLevel


class Track:
    """Logger class used to configure and handle logging activities.

    This class is designed to manage log records through the Loguru logging library. It includes mechanisms to set up
    custom logging configurations, use hierarchical handling through parent and child loggers, and perform logging at
    various levels with enriched metadata.

    Attributes:
        __handler (Handler): The handler instance associated with the logger, indicating the type of handling performed.
        __handler_uuid (str): Unique identifier for the current handler.
        __parent_handler_uuid (str | None): Identifier for the parent handler, if applicable.
        _logger: The Loguru logger instance used for logging.
    """

    def __init__(self, handler: Handler, parent_handler_uuid: str | None = None, **kwargs: Any) -> None:
        """Logger class init method."""
        self.__handler: Handler = handler
        self.__handler_uuid: str = kwargs.get(Constants.HANDLER_UUID_KEY, "")
        self.__parent_handler_uuid: str | None = parent_handler_uuid
        self._logger = logger

        # initialize with default sink
        self.__handler_default_sink_configuration()

    def __handler_default_sink_configuration(self) -> None:
        """Set the configuration for Reporter sink."""
        self._logger.bind(
            event_uuid="",
            parent_handler_uuid="",
            parent_uuid="",
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

    async def report(self, level: LoggerLevel | TrackerLevel | TrackerGroup, message: str, **kwargs: Any) -> None:
        """Unique point to apply changes and log."""
        now_utc: str = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        self._logger.log(
            level.name,
            message,
            event_uuid=generate_uuid4(),
            parent_handler_uuid=self.__parent_handler_uuid,
            handler_uuid=self.__handler_uuid,
            handler_type=self.__handler.name,
            generated_utc_timestamp=now_utc,
            **kwargs,
        )
