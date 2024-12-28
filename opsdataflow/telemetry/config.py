"""Sets the configuration to use Telemetry module."""

from dataclasses import dataclass


@dataclass
class SignalsConfig:
    """Telemetry."""

    environment: str
    app_name: str
    output_format: str | None = None
    log_from_level: int = 0
    parent_uuid: str | None = None
    use_singleton_design_pattern: bool = True
