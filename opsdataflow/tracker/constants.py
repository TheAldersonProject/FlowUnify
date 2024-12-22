# type: ignore[reportAttributeAccessIssue]
# type: ignore[reportUnknownMemberType]
# type: ignore[reportUnknownVariableType]
"""Tracker project constants."""

from typing import Any, ClassVar

from opsdataflow.tracker.enums import Handler


class Constants:
    """Constants class for defining keys and default values used across the application.

    The Constants class is a centralized location for storing various string constants and default configuration
    values used in the application. The keys and their associated default values are frequently used for
    initializing handlers, logging configurations, and ensuring consistent formatting.

    Attributes:
        HANDLER_UUID_KEY (str): Key used to represent the handler's unique identifier.

        LOGGER_SINK_FORMAT_KEY (str): Key used to represent the format of the logger's sink.

        LOGGER_EXTRA_KEY (str): Key used to hold extra logging information.

        LOGGER_SINK_FORMAT_DEFAULT_VALUE (str): Default format string for logger sink output, defining how time, level,
            and other message details are displayed.

        DEFAULT_CONFIGURATIONS (ClassVar[dict[Any, dict[str, Any]]]): A dictionary that provides default configurations
            for handlers. It includes default values for logger-related keys such as `LOGGER_SINK_FORMAT_KEY` and
            `LOGGER_EXTRA_KEY`.
    """

    # handlers keys
    HANDLER_UUID_KEY: str = "handler_uuid"

    # logger keys
    LOGGER_SINK_FORMAT_KEY: str = "logger_sink_format"
    LOGGER_EXTRA_KEY: str = "logger_extra"

    # logger sink default values
    LOGGER_SINK_FORMAT_DEFAULT_VALUE: str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>"
        " | <level>{extra[handler_type]}:{level: <8}</level>"
        " | <level>{message}</level>"
        " | <level>Extra: {extra}</level>"
    )

    # default configurations for the handler
    DEFAULT_CONFIGURATIONS: ClassVar[dict[Any, dict[str, Any]]] = {
        Handler.LOGGER: {
            LOGGER_SINK_FORMAT_KEY: LOGGER_SINK_FORMAT_DEFAULT_VALUE,
            LOGGER_EXTRA_KEY: [],
        },
    }
