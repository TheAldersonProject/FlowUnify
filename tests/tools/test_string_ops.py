# tests/test_string_ops.py
"""Tests for string_ops.py."""

from opsdataflow.tools.string_ops import is_empty


def test_is_empty_with_none() -> None:
    """Test that is_empty returns True for None."""
    assert is_empty(None) is True


def test_is_empty_with_empty_string() -> None:
    """Test that is_empty returns True for an empty string."""
    assert is_empty("") is True


def test_is_empty_with_whitespace_string() -> None:
    """Test that is_empty returns True for a string containing only whitespace."""
    assert is_empty("   ") is True


def test_is_empty_with_non_empty_string() -> None:
    """Test that is_empty returns False for a non-empty string."""
    assert is_empty("hello") is False


def test_is_empty_with_string_containing_whitespace_and_characters() -> None:
    """Test that is_empty returns False for a string containing characters and whitespace."""
    assert is_empty("  hello  ") is False


def test_is_empty_with_numeric_string() -> None:
    """Test that is_empty returns False for a numeric string."""
    assert is_empty("123") is False


def test_is_empty_with_special_characters() -> None:
    """Test that is_empty returns False for a string containing special characters."""
    assert is_empty("@#$%^") is False
