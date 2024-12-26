from opsdataflow.telemetry.enums import LoggerLevel
from opsdataflow.telemetry.signals_previous_implementation import Signals

tracker_sink_format: str = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>"
    " | <level>{level: <8}</level>"
    " | <level>{message}</level>"
    # " | <level>Extra: {extra}</level>"
)
tracker = Signals(tracker_sink_format=tracker_sink_format)
tracker.add_sink_setup(
    sink="../../sink/my22.log",
    format="{extra[serialized]}",
    level=LoggerLevel.TRACE.value,
    enqueue=True,
    catch=False,
    serialize=True,
)

tracker.process(
    name="I am a process. My name is ProcessMe.",
    description="My description",
    parent_uuid="123"
)
tracker.task(name="I am a task.", description="Task description")
tracker.step(
    name="I am a step. My name is StepMe.",
    description="My description",
    step_parent_uuid="123")
tracker.trace("Trace me down.")
tracker.debug("Bug me up.")
tracker.info("Info-me.")
tracker.end_step()
tracker.end_process()
tracker.warning("Life without a warning.")
tracker.error("You've got error.")
tracker.end_process()
tracker = Signals()
tracker.trace("1 - Hello World Trace!")
tracker.debug("2 - Hello World Debug!")
tracker.info("3 - Hello World Info!")
tracker.business("I'll give you the context!")
tracker.warning("4 - Hello World Warning!")
tracker.error("5 - Hello World Error!", additional="Oh my gosh, an error!!!")
tracker.step()

# tracker.end_step()
# tracker.event("Back to task")
# tracker.step()
# tracker.event("I am a new kid step")
# tracker.end_task()
# tracker.event("I should be a process event.")

# tracker.process(
#     process_name="I am another process. My name is ProcessMe Again.",
#     process_description="My description is different.",
#     process_parent_uuid=None
# )
# tracker.event("I am a new event.")



