from typing import Any

from loguru import logger
from opsdataflow.track_flow.enums import Handler
from opsdataflow.track_flow.handler_configuration import HandlerConfiguration

# using default values
parameters: dict[str, Any] = HandlerConfiguration(Handler.LOGGER).configure()
logger.debug(f"Parameters: {parameters}")

# Providing configuration
parameters: dict[str, Any] = HandlerConfiguration(Handler.LOGGER).configure(
    my_var="some var.",
    my_other_var="some other var."
)
logger.debug(f"Parameters: {parameters}")
