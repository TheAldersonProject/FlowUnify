"""Some examples for logger handler without configuration."""  # noqa: INP001
from opsdataflow.track_flow.logger import Logger

sink_format: str = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>"
    " | <level>{extra[handler_type]}:{level: <8}</level>"
    " | <level>🚀{message}</level>"
)
_logger = Logger(logger_sink_format=sink_format)
_logger.trace("1 - Hello World Trace!")
_logger.debug("2 - Hello World Debug!")
_logger.info("3 - Hello World Info!")
_logger.warning("4 - Hello World Warning!")
_logger.error("5 - Hello World Error!")
_logger.critical("6 - Hello World Critical!")
