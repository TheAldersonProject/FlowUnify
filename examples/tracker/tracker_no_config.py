from opsdataflow.event_track.tracker import Tracker

tracker = Tracker()
tracker.process(
    name="I am a process. My name is ProcessMe.",
    description="My description",
    parent_uuid="123"
)
tracker.task()
tracker.step(
    name="I am a step. My name is StepMe.",
    description="My description",
    step_parent_uuid="123")
tracker.end_step()
tracker.process()
tracker.step()
tracker.end_task()
tracker.business("hi")

# tracker.process(
#     process_name="I am another process. My name is ProcessMe Again.",
#     process_description="My description is different.",
#     process_parent_uuid=None
# )
# tracker.event("I am a new event.")
