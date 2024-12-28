from opsdataflow.telemetry.signals import Signals, SignalsConfig

t = SignalsConfig(app_name="My little app.", environment="Dreamland")
tracker = Signals(t)
tracker.process(
    title="I am a process. My name is ProcessMe.",
    summary="My description",
)
tracker.step(
    title="I am a step. My name is StepMe.",
    summary="My description",
)
tracker.business("hi")
