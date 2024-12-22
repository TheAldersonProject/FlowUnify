"""Some examples for logger handler without configuration."""  # noqa: INP001
from opsdataflow.track_flow.logger import Logger

_logger = Logger()
_logger.trace("1 - Hello World Trace!")
_logger.debug("2 - Hello World Debug!")
_logger.info("3 - Hello World Info!")
_logger.warning("4 - Hello World Warning!")
_logger.error("5 - Hello World Error!")
_logger.critical("6 - Hello World Critical!")

try:
    ret = 1/0
except Exception as e:  # noqa: BLE001
    _logger.critical("Error", exc_info=e)
