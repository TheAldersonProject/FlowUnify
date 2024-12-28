"""Example of signals usage."""  # noqa: INP001

from opsdataflow.telemetry import Signals, SignalsConfig

output: str = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>"
    " | <level>{level: <8}</level>"
    " | <level>{message}</level>"
    " | <level>Extra: {extra}</level>"
)
t = SignalsConfig(app_name="MyExample", environment="Dev-Environment", output_format=output)
tracker = Signals(config=t)

tracker.process(
    title="I am a process. My name is ProcessMe.",
    summary="My description",
)
tracker.task(title="I am a task.", summary="Task description")
tracker.step(title="I am a step. My name is StepMe.", summary="My description")
tracker.trace("Trace me down.")
tracker.debug("Bug me up.")
tracker.info("Info-me.")
tracker.warning("Life without a warning.")
tracker.error("You've got error.")
tracker.trace("1 - Hello World Trace!")
tracker.debug("2 - Hello World Debug!")
tracker.info("3 - Hello World Info!")
tracker.business("I'll give you the context!")
tracker.warning("4 - Hello World Warning!")
tracker.error("5 - Hello World Error!", additional="Oh my gosh, an error!!!")

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
