"""Handlers configuration."""

from copy import deepcopy
from typing import Any

from loguru import logger

from opsdataflow.tools import uuid
from opsdataflow.track_flow.constants import Constants
from opsdataflow.track_flow.enums import Handler


class HandlerConfiguration:
    """Handles application configuration setup and management.

    This class provides functionality to manage application settings, including initializing default configurations,
    customizing configurations, and generating unique process identifiers. The configuration is primarily managed
    through a dictionary with predefined keys and values. It also supports additional custom settings through
    an extras section.
    """

    def __init__(self, handler: Handler) -> None:
        """Initializes the configuration for a specific handler.

        This function sets up the configuration for a given handler by performing a deep copy of the
        default configurations. The default configuration is determined based on the provided handler
        and ensures that the original default configurations remain unmodified.

        Args:
            handler: A Handler instance whose specific configuration should be initialized.
        """
        self._configuration: dict[str, Any] = deepcopy(Constants.DEFAULT_CONFIGURATIONS[handler])

    def build(self, **kwargs: Any) -> dict[str, Any]:
        """Builds the handler with the provided settings.

        This method accepts dynamic keyword arguments to configure a handler instance. It validates the provided keys
        against a predefined configuration dictionary.
        If a key matches the predefined configuration, its value is updated; otherwise, unrecognized keys
        are stored as extra settings. The method also generates a unique identifier (UUID) for the handler instance.

        Args:
            kwargs: Variable keyword arguments representing the configuration options.

        Returns:
            A dictionary containing the configured settings, including updated values and extras.
        """
        if not kwargs:
            logger.debug("No information provided for configuration.")
            logger.debug("Default values will be applied.")

        else:
            params: dict[str, Any] = dict(**kwargs)
            logger.debug(f"Config keys: {params.keys()}")

            for k, v in params.items():
                clean_key: str = str(k).lower().strip()
                logger.debug(f"Validating key: {clean_key}.")
                if clean_key in self._configuration:
                    self._configuration[clean_key] = v
                    logger.debug(f"Key <{clean_key}> set with value of type: <{type(v)}>")
                else:
                    logger.debug(f"Key '{k}' not found in default configuration, will be added to extras.")
                    self._configuration[Constants.LOGGER_EXTRA_KEY].append({clean_key: v})

        self._configuration[Constants.HANDLER_UUID_KEY] = uuid.generate_uuid4()
        logger.debug(
            f"Handler configuration set for handler type: {Handler.LOGGER.name} "
            f"with UID: {self._configuration[Constants.HANDLER_UUID_KEY]}"
        )

        return self._configuration
