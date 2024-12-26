"""Establishes a Protocol for Signals usage."""

from typing import Any, Protocol


class Telemetry(Protocol):
    """Protocol for telemetry and logging functions.

    This class defines a protocol for telemetry logging methods. It includes methods for different logging levels
    (trace, debug, info, warning, error, exception) that allow capturing log messages with varying degrees of
    severity and detail. These methods are intended to be implemented by any class adhering to this protocol.

    The protocol ensures that logs are consistent in format, provide contextual details through optional keyword
    arguments, and accommodate logging requirements across various logging levels. Classes implementing this
    protocol can be used in systems where detailed logging functionality is required.
    """

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
        ...

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
        ...

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
        ...

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
        ...

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
        ...

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
        ...

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
        ...
