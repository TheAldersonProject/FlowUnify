from opsdataflow.track_flow.tracker import Tracker

tracker = Tracker()
tracker.process(
    process_name="I am a process. My name is ProcessMe.",
    process_description="My description",
    process_parent_uuid="123"
)
tracker.event("I am an event.")
tracker.task()
tracker.event("I am an event of a task type.")
tracker.step(
    step_name="I am a step. My name is StepMe.",
    step_description="My description",
    step_parent_uuid="123")
tracker.event("I am an event of a task type.")
tracker.end_step()
tracker.event("Back to task")
tracker.step()
tracker.event("I am a new kid step")
tracker.end_task()
tracker.event("I should be a process event.")

# tracker.process(
#     process_name="I am another process. My name is ProcessMe Again.",
#     process_description="My description is different.",
#     process_parent_uuid=None
# )
# tracker.event("I am a new event.")
