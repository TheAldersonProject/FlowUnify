"""Tools for working with strings."""


def is_empty(value: str | None) -> bool:
    """Check if a string is empty or contains only whitespace.

    This function determines whether a given string is empty, contains only whitespace,
    or is None. It returns a boolean result indicating whether the value meets these
    conditions.

    Args:
        value: The string to check. Can be None.

    Returns:
        bool: True if the string is None, empty, or contains only whitespace; otherwise, False.
    """
    value = value.strip() if value else None
    return not value
