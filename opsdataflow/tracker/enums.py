# whoami: src/tracker/enums.py
"""Collection of Enum classes to be used for Tracker library."""

from enum import IntEnum
from typing import NamedTuple


class EventLevel(NamedTuple):
    """Event Levels."""

    name: str
    value: int


class TrackerSeverityLevel(IntEnum):
    """Severity Levels."""

    # Default implementation
    TRACE = 5  # Detailed information for debugging
    DEBUG = 10  # Diagnostic information
    INFO = 20  # General operational information
    SUCCESS = 25  # Successful completion of operations
    WARNING = 30  # Potential issues that don't affect core functionality
    ERROR = 40  # Recoverable errors that affect functionality
    CRITICAL = 50  # Unrecoverable errors that require immediate attention

    # Tracker Implementation
    EVENT = 55  # Event itself
    BUSINESS = 60  # Events related to business
    DEVOPS = 65  # Events related to DevOps
    DATA_SOURCE = 70  # Events related to data sources
    DATA_SET = 75  # Events related to datasets
    DATAOPS = 80  # Events related
    SECURITY = 100  # Events related to security

    def __str__(self) -> str:
        """Overwrites the __str__ method to retrieve the name.title() of the severity level."""
        return self.name.title()

    def as_tuple(self) -> EventLevel:
        """Retrieves the log level name and value as a NamedTuple."""
        return EventLevel(self.name, self.value)
