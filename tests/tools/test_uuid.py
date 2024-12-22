# File: tests/test_uuid.py

import uuid

from opsdataflow.tools.uuid import generate_uuid4


def test_generate_uuid4_returns_valid_uuid() -> None:
    """Test that generate_uuid4 returns a valid UUID version 4."""
    result = generate_uuid4()
    assert uuid.UUID(result).version == 4


def test_generate_uuid4_is_unique() -> None:
    """Test that generate_uuid4 generates unique UUIDs."""
    uuid1 = generate_uuid4()
    uuid2 = generate_uuid4()
    assert uuid1 != uuid2
