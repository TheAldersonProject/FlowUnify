"""Tools for working with strings."""

import hashlib

from tools.uuid import generate_uuid4


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


def obfuscate_string_using_secure_hash(value: str, secure_hash_text: str) -> str:
    """Obfuscate string using MD5 and a secure hash."""
    _value = value or generate_uuid4() + secure_hash_text
    return hashlib.md5(str(_value).encode("utf-8")).hexdigest()  # noqa: S324
