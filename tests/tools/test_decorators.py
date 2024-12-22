# File: tests/test_decorators.py

from opsdataflow.tools.decorators import singleton


def test_singleton_creates_single_instance() -> None:
    """Test that the singleton decorator creates only one instance of a class."""
    @singleton
    class TestClass:
        pass

    instance1 = TestClass()
    instance2 = TestClass()

    assert instance1 is instance2


def test_singleton_with_constructor_args() -> None:
    """Test that arguments passed to the class constructor are respected."""
    @singleton
    class TestClass:
        def __init__(self, value: int) -> None:
            self.value = value

    instance1 = TestClass(10)
    instance2 = TestClass(20)

    assert instance1 is instance2
    assert instance1.value == 10  # Constructor args only used on the first call


def test_singleton_thread_safety() -> None:
    """Test that the singleton decorator is thread-safe."""
    import threading

    @singleton
    class TestClass:
        def __init__(self, value: int) -> None:
            self.value = value

    def create_instance(value: int) -> TestClass:
        return TestClass(value)

    thread1 = threading.Thread(target=create_instance, args=(1,))
    thread2 = threading.Thread(target=create_instance, args=(2,))

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    instance1 = TestClass(3)
    assert instance1.value in (1, 2)  # Confirm only one instance exists


def test_singleton_with_multiple_classes() -> None:
    """Test singleton behavior when applied to multiple classes."""
    @singleton
    class ClassA:
        pass

    @singleton
    class ClassB:
        pass

    instance_a1 = ClassA()
    instance_a2 = ClassA()
    instance_b1 = ClassB()
    instance_b2 = ClassB()

    assert instance_a1 is instance_a2
    assert instance_b1 is instance_b2
    assert instance_a1 is not instance_b1