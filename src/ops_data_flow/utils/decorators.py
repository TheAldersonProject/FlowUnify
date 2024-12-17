#whoami: examples/ops_data_flow/utils/decorators.py
"""OpsDataFlow Decorators."""

import threading
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

T = TypeVar("T")  # Type variable to maintain type hints
P = ParamSpec("P")

_lock = threading.RLock()  # lock to ensure thread safety

def singleton(cls: type[T]) -> Callable[..., T]:
    """Create and maintain a single instance of an object.

    Args:
        cls: The class to apply the singleton pattern to.

    Returns:
        A decorated class instance that ensures only one instance of the class is created.
    """
    instances = {}

    @wraps(cls)
    def get_instance(*args: P.args, **kwargs: P.kwargs) -> T:
        with _lock:  # acquire lock to ensure thread safety
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
            return instances[cls]  # pyright: ignore[reportUnknownVariableType]

    return get_instance
