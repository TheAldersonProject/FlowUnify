"""Logger handler."""

import json
from copy import deepcopy
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

        def serialize(record: Any) -> str:
            """Serialize the record."""
            _record_extra: dict[str, Any] = deepcopy(record["extra"])
            if "serialized" in _record_extra:
                del _record_extra["serialized"]

            def get_extra_values(key: str) -> Any:
                """Get the value of the extra key."""
                if key not in _record_extra:
                    return "Not found"

                value = _record_extra.get(key, "")
                del _record_extra[key]
                return value

            common_header: dict[str, Any] = {
                "utc_timestamp": get_extra_values("generated_utc_timestamp"),
                "parent_uuid": get_extra_values("parent_uuid"),
                "process_uuid": get_extra_values("process_uuid"),
            }

            common_additional_information: dict[str, Any] = {
                "handler_type": get_extra_values("handler_type"),
                "reported_message": record["message"],
                "handler_uuid": get_extra_values("handler_uuid"),
                "time_elapsed": str(record["elapsed"]),
            }

            subset: dict[str, Any] = {
                "event_type": record["level"].name,
                "uuid": get_extra_values("event_uuid"),
                "header": {} | common_header,
                "additional_information": {} | common_additional_information,
            }

            if record["level"].name in [TrackerGroup.PROCESS.name, TrackerGroup.TASK.name, TrackerGroup.STEP.name]:
                subset |= {
                    "data": {
                        "name": get_extra_values("name"),
                        "description": get_extra_values("description"),
                    }
                }
            elif record["level"].name == TrackerLevel.BUSINESS.name:
                subset |= {
                    "data": {
                        "context": get_extra_values("business_context"),
                    }
                }
            else:
                subset |= {
                    "data": {
                        "log": record.get("message", "Not informed"),
                    }
                }

            subset |= {"extra-values": _record_extra}
            return json.dumps(subset)

        def patching(record: Any) -> None:
            """Patch the record."""
            record["extra"]["serialized"] = serialize(record)

        # removes the default handler
        self._logger.remove(0)
        self._logger = logger.patch(patching)

    @property
    def handler_uuid(self) -> str:
        """Returns the handler UUID."""
        return self.__handler_uuid

    @property
    def reporter(self) -> Any:
        """Returns the Loguru Logger instance."""
        return self._logger

    async def report(
        self,
        level: LoggerLevel | TrackerLevel | TrackerGroup,
        message: str,
        handler: Handler | None = None,
        **kwargs: Any,
    ) -> None:
        """Unique point to apply changes and log."""
        now_utc: str = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        self._logger.log(
            level.name,
            message,
            event_uuid=generate_uuid4(),
            parent_handler_uuid=self.__parent_handler_uuid,
            handler_uuid=self.__handler_uuid,
            handler_type=handler.name if handler else self.__handler.name,
            generated_utc_timestamp=now_utc,
            **kwargs,
        )
