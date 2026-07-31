import pytest
from unittest.mock import MagicMock
from sagittarius_engine.interfaces import IContainer, IEventBus

def test_context_class_initialization():
    from sagittarius_engine.kernel.context import Context

    # Save original abstract methods to avoid test pollution
    original_abstract_methods = Context.__abstractmethods__
    try:
        # Disable abstract methods check to allow instantiation of the snippet class
        Context.__abstractmethods__ = frozenset()

        app_mock = MagicMock()
        container_mock = MagicMock(spec=IContainer)
        event_bus_mock = MagicMock(spec=IEventBus)

        # Act
        context = Context(app=app_mock, container=container_mock, event_bus=event_bus_mock)

        # Assert exactly what is in the snippet
        assert getattr(context, "_container", None) is container_mock

    finally:
        # Restore abstract methods
        Context.__abstractmethods__ = original_abstract_methods
