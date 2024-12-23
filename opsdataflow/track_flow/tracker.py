"""Tracker handler."""

import asyncio
import sys
from typing import Any

from opsdataflow.tools import singleton
from opsdataflow.tools.uuid import generate_uuid4
from opsdataflow.track_flow.constants import Constants
from opsdataflow.track_flow.enums import Handler, TrackerGroup, TrackerLevel
from opsdataflow.track_flow.handler_configuration import HandlerConfiguration
from opsdataflow.track_flow.track_handler import Track


@singleton
class Tracker(Track):
    """Tracker class."""

    def __init__(self, **kwargs: Any) -> None:
        """Logger class init method."""
        self.__parameters: dict[str, Any] = HandlerConfiguration(Handler.TRACKER).build(**kwargs)
        super().__init__(
            handler=Handler.TRACKER,
            handler_uuid=self.__parameters.get(Constants.HANDLER_UUID_KEY, generate_uuid4()),
            **kwargs,
        )
        # process information
        self.__process_uuid: str | None = None
        self.__name: str | None = None
        self.__description: str | None = None
        self.__parent_uuid: str | None = None

        # task information
        self.__task_uuid: str | None = None

        # step information
        self.__step_uuid: str | None = None

        # main information
        self.__current_group_uuid: str | None = None
        self.__event_of_type: TrackerLevel | TrackerGroup = TrackerGroup.PROCESS

        self.__sink_basic_configuration()
        self.__set_event_level()
        self.__set_group_levels()

    def __set_group_levels(self) -> None:
        """Sets all the group levels."""
        super().reporter.level(
            name=TrackerGroup.PROCESS.name, no=TrackerGroup.PROCESS.value, color="<green>", icon="✨"
        )
        super().reporter.level(name=TrackerGroup.TASK.name, no=TrackerGroup.TASK.value, color="<yellow>", icon="🗒️")
        super().reporter.level(name=TrackerGroup.STEP.name, no=TrackerGroup.STEP.value, color="<cyan>", icon="👣️")

    def __set_event_level(self) -> None:
        """Set the configuration for Tracker levels."""
        super().reporter.level(name=TrackerLevel.EVENT.name, no=TrackerLevel.EVENT.value, color="<blue>", icon="✨")

    def __sink_basic_configuration(self, **kwargs: Any) -> None:
        """Set the configuration for Reporter sink."""
        # default sink to sys.stdout
        super().reporter.add(
            sink=sys.stdout,
            level=TrackerLevel.EVENT.value,
            format=self.__parameters[Constants.TRACKER_SINK_FORMAT_KEY],
            filter=None,
            colorize=True,
            serialize=False,
            backtrace=True,
            diagnose=True,
            enqueue=False,
            context=None,
            catch=True,
            **kwargs,
        )

    def event(self, message: str, **kwargs: Any) -> None:
        """Report an event asynchronously.

        This method is designed to report a specific event by taking in a message and optional keyword arguments.
        It uses the asynchronous `super().report(...)` method to handle the reporting of the event with
        the given parameters, executing it using `asyncio.run`.

        Args:
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

        asyncio.run(
            super().report(
                self.__event_of_type,
                message,
                process_uuid=self.__process_uuid,
                event_of_type=self.__event_of_type.name.title(),
                **kwargs,
            )
        )

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

        self.__event_of_type = group
        self.__current_group_uuid = event_group_uuid
        self.event(
            uuid=event_group_uuid,
            message=event_greeting,
            parent_uuid=self.__parent_uuid,
            name=self.__name,
            description=self.__description,
            **kwargs,
        )

    def process(
        self,
        process_name: str | None = None,
        process_description: str | None = None,
        process_parent_uuid: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Starts the process tracking group."""
        self.__start_group(
            group=TrackerGroup.PROCESS,
            name=process_name,
            description=process_description,
            parent_uuid=process_parent_uuid,
            **kwargs,
        )

    def task(self, task_name: str | None = None, task_description: str | None = None, **kwargs: Any) -> None:
        """Starts the task tracking group."""
        self.__start_group(group=TrackerGroup.TASK, name=task_name, description=task_description, **kwargs)

    def step(self, step_name: str | None = None, step_description: str | None = None, **kwargs: Any) -> None:
        """Starts the step tracking group."""
        self.__start_group(group=TrackerGroup.STEP, name=step_name, description=step_description, **kwargs)

    def end_step(self) -> None:
        """Ends the step tracking group."""
        if self.__step_uuid:
            self.__step_uuid = None
            self.__current_group_uuid = self.__task_uuid or self.task()
            self.__event_of_type = TrackerGroup.TASK

    def end_task(self) -> None:
        """Ends the task tracking group."""
        if self.__task_uuid:
            self.end_step()
            self.__task_uuid = None
            self.__current_group_uuid = self.__process_uuid or self.process()
            self.__event_of_type = TrackerGroup.PROCESS

    def end_process(self) -> None:
        """Ends the process tracking group."""
        if self.__process_uuid:
            self.end_task()
            self.__process_uuid = None
            self.__current_group_uuid = None
