"""UUID Generator and management."""

import uuid


def generate_uuid4() -> str:
    """Generate a universally unique identifier (UUID) version 4.

    This function creates and returns a string representation of a random UUID
    (version 4) using the `uuid` module. Version 4 UUIDs are generated using random
    numbers, ensuring the uniqueness of the identifier without requiring any input
    parameters.

    Returns:
        str: A string representation of a randomly generated UUID version 4.
    """
    return str(uuid.uuid4())


def generate_uuid5(namespace: str, name: str) -> str:
    """Generate a UUID version 5 string.

    This function generates a UUID version 5 (SHA-1 hash-based) by combining a namespace
    with a given name. The namespace and name are concatenated to create a unique input,
    and a UUID is computed using the uuid5 method from the uuid module.

    Args:
        namespace: A string representing the namespace to use for UUID generation.
        name: A string representing the name to combine with the namespace for UUID generation.

    Returns:
        A string representing the generated UUID version 5.
    """
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, namespace + name))
