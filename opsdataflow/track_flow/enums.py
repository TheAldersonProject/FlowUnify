"""Tracker project common enums."""

from enum import IntEnum
from typing import NamedTuple


class Level(NamedTuple):
    """Defines a named tuple EventLevel for categorizing levels."""

    name: str
    value: int


class LoggerLevel(IntEnum):
    """Enumeration for Logger Severity Levels.

    This enumeration defines various levels of logging severity to classify log
    messages based on their importance and urgency. It extends `IntEnum` and
    maps each severity level to an integer value commonly used in logging frameworks.
    These levels enable fine-grained control over log message filtering and categorization.

    The levels include:
    - TRACE: Provides the most detailed information, useful during development and debugging.
    - DEBUG: Captures diagnostic information needed to analyze the code's behavior or state.
    - INFO: Represents general informational messages about system operations.
    - WARNING: Highlights potential issues that could escalate into errors but does not affect
      current functionality.
    - ERROR: Refers to recoverable errors that may lead to incorrect application behavior.
    - CRITICAL: Denotes severe errors that require immediate intervention to avoid further impact.
    """

    TRACE = 5  # Detailed information for debugging
    DEBUG = 10  # Diagnostic information
    INFO = 20  # General operational information
    WARNING = 30  # Potential issues that don't affect core functionality
    ERROR = 40  # Recoverable errors that affect functionality
    CRITICAL = 50  # Unrecoverable errors that require immediate attention

    def __str__(self) -> str:
        """Overwrites the __str__ method to retrieve the name.title() of the severity level."""
        return self.name.title()

    def as_tuple(self) -> Level:
        """Retrieves the log level name and value as a NamedTuple."""
        return Level(self.name, self.value)


class TrackerLevel(IntEnum):
    """TrackerSeverityLevel Enumeration.

    Defines various severity levels for tracking events in an application. These severity levels are grouped
    based on their context such as events, business operations, DevOps, data sources, datasets, data operations,
    and security.

    Attributes:
        EVENT (int): Event itself.
        BUSINESS (int): Events related to business.
        DEVOPS (int): Events related to DevOps.
        DATA_SOURCE (int): Events related to data sources.
        DATA_SET (int): Events related to datasets.
        DATAOPS (int): Events related to data operations.
        SECURITY (int): Events related to security.
    """

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

    def as_tuple(self) -> Level:
        """Retrieves the log level name and value as a NamedTuple."""
        return Level(self.name, self.value)


class TrackerGroup(IntEnum):
    """Enumeration to define tracker groups for event categorization.

    This class defines various groups for organizing and categorizing events based on their context such as processes,
    tasks, and steps. Each group is associated with an integer value and has a predefined hierarchy for better
    classification.

    Attributes:
        PROCESS (int): Represents a process encompassing multiple events.
        TASK (int): Groups specific events under a predefined task context.
        STEP (int): Groups events under a specific step, requiring a parent task for categorization.
    """

    PROCESS = 120  # Process to group all events.
    TASK = 110  # Groups specific events under a pre-defined task.
    STEP = 100  # To group all events under a specific step. must have a task to be grouped by.

    def __str__(self) -> str:
        """Overwrites the __str__ method to retrieve the name.title() of the severity level."""
        return self.name.title()

    def as_tuple(self) -> Level:
        """Retrieves the log level name and value as a NamedTuple."""
        return Level(self.name, self.value)


class Handler(IntEnum):
    """Enumeration to define different handler types.

    Defines integer values associated with specific handlers like LOGGER and TRACKER. This class inherits from IntEnum,
    allowing for enumeration of integer constants. It can be used to represent and manipulate handler types in a more
    readable and descriptive way.
    """

    LOGGER = 1
    TRACKER = 2

    def __str__(self) -> str:
        """Overwrites the __str__ method to retrieve the name.title() of the severity level."""
        return self.name.title()
