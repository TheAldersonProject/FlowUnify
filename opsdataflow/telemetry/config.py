"""Sets the configuration to use Telemetry module."""

from dataclasses import dataclass


@dataclass
class TelemetryConfig:
    """Telemetry."""

    output_format: str | None = None
    log_from_level: int = 0
    app_name: str | None = None
    parent_uuid: str | None = None
    use_singleton_design_pattern: bool = True
