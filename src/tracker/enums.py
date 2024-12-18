# whoami: src/tracker/enums.py
"""Collection of Enum classes to be used for YapLogger."""

from enum import IntEnum
from typing import NamedTuple


class LogLevel(NamedTuple):
    """Log Levels."""

    name: str
    value: int


class SeverityLevel(IntEnum):
    """Severity Levels."""

    TRACE = 5  # Detailed information for debugging
    DEBUG = 10  # Diagnostic information
    INFO = 20  # General operational information
    SUCCESS = 25  # Successful completion of operations
    WARNING = 30  # Potential issues that don't affect core functionality
    ERROR = 40  # Recoverable errors that affect functionality
    CRITICAL = 50  # Unrecoverable errors that require immediate attention

    def __str__(self) -> str:
        """Overwrites the __str__ method to retrieve the name.title() of the severity level."""
        return self.name.title()

    def as_tuple(self) -> LogLevel:
        """Retrieves the log level name and value as a NamedTuple."""
        return LogLevel(self.name, self.value)
