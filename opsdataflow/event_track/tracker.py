"""Tracker handler."""

from typing import Any

from opsdataflow.event_track.configuration import Configuration
from opsdataflow.event_track.constants import Constants
from opsdataflow.event_track.enums import Handler, LoggerLevel, TrackerGroup, TrackerLevel
from opsdataflow.tools import singleton
from opsdataflow.tools.uuid import generate_uuid4


@singleton
class Tracker(Configuration):
    """Tracker class."""

    def __init__(self, handler: Handler = Handler.TRACKER, **kwargs: Any) -> None:
        """Logger class init method."""
        # instance configuration
        self.__logger: Any = None
        self.__handler: Handler = handler

        # service configuration
        self.__handler_uuid: str = generate_uuid4()

        # super class initialization
        super().__init__(handler=handler, **kwargs)

        # build general parameters
        self.__parameters: dict[str, Any] = super().build(**kwargs)

        # group general information
        self.__name: str | None = None
        self.__description: str | None = None
        self.__parent_uuid: str | None = None
        self.__current_group_uuid: str | None = None

        # process information -- uuid
        self.__process_uuid: str | None = None

        # task information -- uuid
        self.__task_uuid: str | None = None

        # step information -- uuid
        self.__step_uuid: str | None = None

        # service setup
        self.__tracker_level_setup()
        self.__group_level_setup()

    def add_sink_setup(self, **kwargs: Any) -> None:
        """Adds a sink setup to the reporter."""
        super().reporter.add(**kwargs)

    def __event(self, message: str, event_type: TrackerGroup | TrackerLevel | LoggerLevel, **kwargs: Any) -> None:
        """Report an event asynchronously.

        This method is designed to report a specific event by taking in a message and optional keyword arguments.
        It uses the asynchronous `super().report(...)` method to handle the reporting of the event with
        the given parameters, executing it using `asyncio.run`.

        Args:
            event_type: Type of the event.
            message: A string representing the event message to be reported.
            **kwargs: Additional optional key-value arguments to further describe the event.

        Returns:
            None
        """
        # if process was not yet started, starts it.
        if not self.__process_uuid:
            self.process()

        # establishes the parent_uuid hierarchy if not informed.
        if "parent_uuid" not in kwargs:
            kwargs["parent_uuid"] = self.__current_group_uuid

        super().report(
            level=event_type,
            message=message,
            handler=self.__handler,
            process_uuid=self.__process_uuid,
            **kwargs,
        )

    def __group_level_setup(self) -> None:
        """Sets the group levels for the reporter.

        This method defines the levels of grouping used within the tracker system and assigns properties such as names,
        numeric values, colors, and icons to these levels. Each level corresponds to a specific group in the tracker,
        facilitating the visual distinction and organization of processes, tasks, and steps.
        """
        super().reporter.level(
            name=TrackerGroup.PROCESS.name, no=TrackerGroup.PROCESS.value, color="<green>", icon="✨"
        )
        super().reporter.level(name=TrackerGroup.TASK.name, no=TrackerGroup.TASK.value, color="<yellow>", icon="🗒️")
        super().reporter.level(name=TrackerGroup.STEP.name, no=TrackerGroup.STEP.value, color="<cyan>", icon="👣️")

    def __tracker_level_setup(self) -> None:
        """Sets the tracker levels for the reporter."""
        super().reporter.level(name=TrackerLevel.BUSINESS.name, no=TrackerLevel.BUSINESS.value, color="<magenta>")

    def __start_group(
        self,
        group: TrackerGroup,
        name: str | None = None,
        description: str | None = None,
        parent_uuid: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Starts tracking group."""

        # sets the main information
        def get_param_value(param: str | None, def_key: str, def_val: str) -> str | None:
            """Returns default value if param is None."""
            return param or self.__parameters.get(def_key, def_val)  # pyright: ignore [reportUnknownVariableType, reportCallIssue]

        # sets the specific and detailed information
        event_greeting: str = ""
        event_group_uuid: str = generate_uuid4()
        match group:
            case TrackerGroup.PROCESS:
                # sets name and description
                self.__name = get_param_value(
                    name, Constants.TRACKER_PROCESS_NAME_KEY, Constants.TRACKER_DEFAULT_PROCESS_NAME
                )
                self.__description = get_param_value(
                    description,
                    Constants.TRACKER_PROCESS_DESCRIPTION_KEY,
                    Constants.TRACKER_DEFAULT_PROCESS_DESCRIPTION,
                )
                # process flow control
                self.__parent_uuid = parent_uuid
                self.__process_uuid = event_group_uuid

                # event message for the process
                event_greeting = (
                    f"Process started: {self.__name} Description: {self.__description} " f"UUID: {event_group_uuid}"
                )

            case TrackerGroup.TASK:
                if not self.__process_uuid:
                    self.process()

                # sets name and description
                self.__name = get_param_value(
                    name, Constants.TRACKER_TASK_NAME_KEY, Constants.TRACKER_DEFAULT_TASK_NAME
                )
                self.__description = get_param_value(
                    description, Constants.TRACKER_TASK_DESCRIPTION_KEY, Constants.TRACKER_DEFAULT_TASK_DESCRIPTION
                )
                # task flow control
                self.__parent_uuid = self.__process_uuid
                self.__task_uuid = event_group_uuid
                event_greeting = (
                    f"Task started: {self.__name} Description: {self.__description} " f"UUID: {event_group_uuid}"
                )

            case TrackerGroup.STEP:
                if not self.__task_uuid:
                    self.task()

                # sets name and description
                self.__name = get_param_value(
                    name, Constants.TRACKER_STEP_NAME_KEY, Constants.TRACKER_DEFAULT_STEP_NAME
                )
                self.__description = get_param_value(
                    description, Constants.TRACKER_STEP_DESCRIPTION_KEY, Constants.TRACKER_DEFAULT_STEP_DESCRIPTION
                )

                self.__parent_uuid = self.__task_uuid
                self.__step_uuid = event_group_uuid
                event_greeting = (
                    f"Step started: {self.__name} Description: {self.__description} " f"UUID: {event_group_uuid}"
                )

        self.__current_group_uuid = event_group_uuid
        self.__event(
            event_type=group,
            uuid=event_group_uuid,
            message=event_greeting,
            parent_uuid=self.__parent_uuid,
            name=self.__name,
            description=self.__description,
            **kwargs,
        )

    def process(
        self, name: str | None = None, description: str | None = None, parent_uuid: str | None = None, **kwargs: Any
    ) -> None:
        """Starts the process tracking group."""
        if self.__process_uuid:
            self.end_task()

        self.__start_group(
            group=TrackerGroup.PROCESS,
            name=name,
            description=description,
            parent_uuid=parent_uuid,
            **kwargs,
        )

    def task(self, name: str | None = None, description: str | None = None, **kwargs: Any) -> None:
        """Starts the task tracking group."""
        self.__start_group(group=TrackerGroup.TASK, name=name, description=description, **kwargs)

    def step(self, name: str | None = None, description: str | None = None, **kwargs: Any) -> None:
        """Starts the step tracking group."""
        self.__start_group(group=TrackerGroup.STEP, name=name, description=description, **kwargs)

    def end_step(self) -> None:
        """Ends the step tracking group."""
        if self.__step_uuid:
            self.__step_uuid = None
            self.__current_group_uuid = self.__task_uuid or self.task()

    def end_task(self) -> None:
        """Ends the task tracking group."""
        if self.__task_uuid:
            self.end_step()
            self.__task_uuid = None
            self.__current_group_uuid = self.__process_uuid or self.process()

    def end_process(self) -> None:
        """Ends the process tracking group."""
        if self.__process_uuid:
            self.end_task()
            self.__process_uuid = None
            self.__current_group_uuid = None

    def business(self, message: str, **kwargs: Any) -> None:
        """Encapsulated trace method with automatic UID inclusion."""
        self.__event(event_type=TrackerLevel.BUSINESS, message=message, business_context=message, **kwargs)

    def trace(self, message: str, **kwargs: Any) -> None:
        """Encapsulated trace method with automatic UID inclusion."""
        self.__event(event_type=LoggerLevel.TRACE, message=message, **kwargs)

    def debug(self, message: str, **kwargs: Any) -> None:
        """Encapsulated debug method with automatic UID inclusion."""
        self.__event(event_type=LoggerLevel.DEBUG, message=message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """Encapsulated info method with automatic UID inclusion."""
        self.__event(event_type=LoggerLevel.INFO, message=message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Encapsulated warning method with automatic UID inclusion."""
        self.__event(event_type=LoggerLevel.WARNING, message=message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Encapsulated error method with automatic UID inclusion."""
        self.__event(event_type=LoggerLevel.ERROR, message=message, **kwargs)

    def critical(self, message: str, exc_info: str | Exception | None = None, **kwargs: Any) -> None:
        """Encapsulated critical method with automatic UID inclusion."""
        self.__event(event_type=LoggerLevel.CRITICAL, message=message, exc_info=exc_info, **kwargs)
