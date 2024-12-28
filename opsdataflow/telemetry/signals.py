"""Signals implementation."""

import os
import sys
from datetime import UTC, datetime
from typing import Any

from loki_logger_handler.formatters.loguru_formatter import LoguruFormatter  # pyright: ignore[reportMissingTypeStubs]
from loki_logger_handler.loki_logger_handler import LokiLoggerHandler  # pyright: ignore[reportMissingTypeStubs]

from opsdataflow.telemetry import Constants, LoggerHandler, LoggerLevel, SignalsConfig, SignalsGroup, SignalsLevel
from opsdataflow.tools import generate_uuid4


class Signals:
    """Class for Signals."""

    def __init__(self, config: SignalsConfig, **kwargs: Any) -> None:
        """Initializes Signals."""
        os.environ["LOKI_URL"] = "http://192.168.200.61:3100/loki/api/v1/push"
        self.__config: SignalsConfig = config
        self.__logger = LoggerHandler().logger

        # signal attributes
        # job uuid
        self._job_uuid: str = generate_uuid4()

        # group uuid
        self._process_uuid: str | None = None
        self._task_uuid: str | None = None
        self._step_uuid: str | None = None

        # process control
        self._current_group_uuid: str | None = None
        self._current_group_name: str | None = None

        # setup logger
        self.__setup_logger_main_configurations()
        self.__setup_loki_server(url=os.environ["LOKI_URL"])
        self.__setup_logger_default_output_sink(**kwargs)

        # greeting with job uuid
        self.info(f"Job started with UUID: {self.job_uuid}")

    def __setup_logger_main_configurations(self) -> None:
        """Sets the logger basic configuration."""
        self.__logger = self.__logger.bind(
            app_name=self.__config.app_name,
            event_uuid="",
            job_uuid=self.job_uuid,
            parent_uuid=self.current_group_uuid or self.job_uuid,
            signal_group_name="",
            signal_timestamp=datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        )
        # self.__logger.level("TRACE")
        self.__logger.remove(0)

    def __setup_loki_server(self, url: str) -> None:
        """Setup Loki server access."""
        # sets the LokiLoggerHandler configuration
        custom_handler = LokiLoggerHandler(
            url=url,
            labels={"application": self.__config.app_name, "environment": self.__config.environment},
            label_keys={"job_uuid", "level", "parent_uuid", "signal_group_name"},
            default_formatter=LoguruFormatter(),  # pyright: ignore[reportArgumentType]
        )
        self.__logger.configure(handlers=[{"sink": custom_handler, "serialize": True}])

    def __setup_logger_default_output_sink(self, **kwargs: Any) -> None:
        """Configures a sink for the logger."""
        self.__logger.add(
            sink=sys.stdout,
            level=self.__config.log_from_level,
            format=self.__config.output_format or Constants.SIGNALS_SINK_FORMAT_DEFAULT_VALUE,
            colorize=True,
            serialize=False,
            backtrace=True,
            diagnose=True,
            enqueue=False,
            catch=True,
            **kwargs,
        )

    def log(self, level: str, message: str, event_uuid: str | None = None, **kwargs: Any) -> None:
        """Emit logs."""
        self.__logger.log(
            level,
            message,
            event_uuid=event_uuid or generate_uuid4(),
            parent_uuid=self._current_group_uuid or self.job_uuid or generate_uuid4(),
            signal_group_name=self.current_group_name or "Job",
            **kwargs,
        )

    def __initialize_group(self, group: SignalsGroup, title: str, summary: str, **kwargs: Any) -> None:
        """Starts a new group."""
        _uuid = generate_uuid4()

        self.log(
            event_uuid=_uuid,
            level=group.name,
            message=f"{title} started.",
            summary=summary,
            title=title,
            **kwargs,
        )
        self.current_group_uuid = _uuid
        self.current_group_name = title.title()

    def process(self, title: str, summary: str, **kwargs: Any) -> None:
        """Starts a new Process group."""
        self.__initialize_group(group=SignalsGroup.PROCESS, title=title, summary=summary, **kwargs)

    def task(self, title: str, summary: str, **kwargs: Any) -> None:
        """Starts a new Task group."""
        self.__initialize_group(group=SignalsGroup.TASK, title=title, summary=summary, **kwargs)

    def step(self, title: str, summary: str | None = None, **kwargs: Any) -> None:
        """Starts a new Task group."""
        self.__initialize_group(group=SignalsGroup.STEP, title=title, summary=summary or "", **kwargs)

    @property
    def job_uuid(self) -> str:
        """Returns job uuid."""
        return self._job_uuid

    @property
    def process_uuid(self) -> str | None:
        """Returns the Process UUID or None."""
        return self._process_uuid

    @property
    def task_uuid(self) -> str | None:
        """Returns the Task UUID or None."""
        return self._task_uuid

    @property
    def step_uuid(self) -> str | None:
        """Returns the Step UUID or None."""
        return self._step_uuid

    @property
    def current_group_uuid(self) -> str | None:
        """Returns the current group UUID or None."""
        return self._current_group_uuid

    @current_group_uuid.setter
    def current_group_uuid(self, value: str | None) -> None:
        """Sets the current group UUID."""
        self._current_group_uuid = value

    @property
    def current_group_name(self) -> str | None:
        """Returns the current group name or None."""
        return self._current_group_name

    @current_group_name.setter
    def current_group_name(self, value: str | None) -> None:
        """Sets the current group name."""
        self._current_group_name = value

    def trace(self, message: str, **kwargs: Any) -> None:
        """Logs a trace-level message.

        This method enables logging of messages with trace-level details, which can be used to trace the application's
        execution flow in fine-grained detail. Trace logs help in debugging and understanding deep-level execution,
        although it is commonly used in development or debug environments.

        Args:
            message: The log message string to be written.
            **kwargs: Additional keyword arguments containing context-specific data for the log entry.

        Returns:
            None
        """
        self.log(level="TRACE", message=message, **kwargs)

    def debug(self, message: str, **kwargs: Any) -> None:
        """Logs a debug message with optional keyword arguments.

        This method is used to log debug-level messages to a logging system. It allows for additional contextual
        keyword arguments to be included in the log message. Debug messages are typically used to provide diagnostic
        information useful for debugging during development.

        Args:
            message (str): The debug message to log.
            **kwargs (Any): Optional keyword arguments that provide additional context for the debug message.

        Returns:
            None
        """
        self.log(level="DEBUG", message=message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """Logs an informational message.

        This method is used to log informational messages. It allows the inclusion of additional
        keyword arguments, which are typically used for specifying optional context or metadata.

        Args:
            message (str): The informational message to be logged.
            **kwargs (Any): Arbitrary keyword arguments for additional context or data.

        Returns:
            None
        """
        self.log(level=LoggerLevel.INFO.name, message=message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Logs a warning message with additional context if provided.

        This method is used to log messages with a warning level of severity.
        It can take additional keyword arguments that provide context for the
        warning. The method formats the message and logs it appropriately
        according to the configuration of the logging system in use.

        Args:
            message: The warning message to be logged.
            **kwargs: Arbitrary keyword arguments containing additional context
                or data to be included with the warning message.

        Returns:
            None
        """
        self.log(level="WARNING", message=message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Logs an error message with the provided details.

        This method allows to log an error message with additional contextual information. It accepts a string `message`
        as the main log content and any number of keyword arguments for context.

        Args:
            message: The error message to log.
            **kwargs: Additional keyword arguments containing context or extra data to include in the log.

        Returns:
            None
        """
        self.log(level="ERROR", message=message, **kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        """Log a critical level message.

        This method is used to log a message with the critical severity level, along with any additional
        contextual information provided via keyword arguments. It is typically used to indicate a severe
        issue that has caused the application to be unable to continue running correctly.

        Arguments:
            message: The critical log message text.
            kwargs: Additional contextual information to be included in the log. This can include key-value
            pairs providing more details about the critical incident.

        Returns:
            None
        """
        self.log(level="CRITICAL", message=message, **kwargs)

    def business(self, message: str, **kwargs: Any) -> None:
        """Handles business logic for processing a message with optional keyword arguments.

        This method is responsible for managing and executing the business logic by taking a message and handling any
        optional keyword parameters passed alongside it. The execution of this logic can vary depending on the
        implementation within the method, and it is intended to be customized as needed for specific use cases.

        Args:
            message: The main message or data to be processed as part of the business logic.
            **kwargs: Additional optional keyword arguments that can be used for contextual execution
            of the business logic.

        Returns:
            None
        """
        self.log(level=SignalsLevel.BUSINESS.name, message=message, **kwargs)

    def dataset(self, message: str, **kwargs: Any) -> None:
        """Logs a message at the DATASET level.

        This method logs a message with the log level set as DATASET. It takes a message string and any additional
        keyword arguments, which are passed for context or specific logging configurations.
        This functionality can be useful to track data-related events or activities within the system.

        Args:
            message: The message string to log.
            **kwargs: Additional arguments to include in the log entry.

        Returns:
            None
        """
        self.log(level=SignalsLevel.DATASET.name, message=message, **kwargs)

    def data_source(self, message: str, **kwargs: Any) -> None:
        """Logs a message with the DATA_SOURCE log level.

        This method allows logging messages that signify data source level
        events using the predefined `DATA_SOURCE` level in the logging system.
        The `message` parameter is required, and additional context can be provided
        through keyword arguments.

        Args:
            message (str): The message to log, representing details about the data source event.
            **kwargs (Any): Optional keyword arguments that provide additional context
                or metadata for the log entry.

        Returns:
            None
        """
        self.log(level=SignalsLevel.DATA_SOURCE.name, message=message, **kwargs)

    def docs(self, message: str, **kwargs: Any) -> None:
        """Logs a message at the DOCS level.

        This method allows logging a message with the `DOCS` level, which is a specific log level defined in the system.
        It takes a message string as its main argument and allows for additional keyword arguments for extended
        logging functionality. The logged message uses the `SignalsLevel.DOCS.name` level.

        Args:
          message: The message to be logged.
          **kwargs: Additional keyword arguments for extended logging options or functionality.

        Returns:
          None

        """
        self.log(level=SignalsLevel.DOCS.name, message=message, **kwargs)


if __name__ == "__main__":
    from loguru import logger

    logger.info("start")
    output: str = Constants.SIGNALS_SINK_FORMAT_DEFAULT_VALUE
    t = SignalsConfig(environment="Dev", app_name="Disruptive DataOps Telemetry.", output_format=output)
    s = Signals(config=t)
    # s.add_sink(
    #     sink=f"../../events/{generate_uuid4()}.log",
    #     # format="{extra[serialized]}",
    #     level=0,
    #     enqueue=True,
    #     catch=False,
    #     serialize=True,
    # )
    s.trace("trace message")
    s.debug("debug message")
    s.info("info message")
    s.process(title="X", summary="This is the X process!")
    s.warning("warning message")
    s.error("error message")
    s.step(title="Y", summary="This step is responsible for YXZ.")
    s.critical("critical message", additional="extra data")
    s.process(title="Z", summary="This is the Z process!")
    s.business("business message")
    s.data_source("datasource message")
    s.dataset("dataset message")

    logger.info("end")
