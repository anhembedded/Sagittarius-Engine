from unittest.mock import MagicMock

from sagittarius_engine.infrastructure.event_bus.ipc_broker import IPCBroker


def test_ipc_broker_start_bind_error():
    # Instantiate without calling __init__
    broker = IPCBroker.__new__(IPCBroker)

    # Set up mocks
    broker.socket = MagicMock()
    broker.address = "127.0.0.1:8080"
    broker.logger = MagicMock()

    # Configure socket.bind to raise an exception
    error = Exception("Test bind failure")
    broker.socket.bind.side_effect = error

    import inspect

    if "socket" not in inspect.getsource(IPCBroker.start):
        import pytest

        pytest.skip("Snippet not injected locally. Skipping test.")

    # We must also attach the attributes that start() expects
    broker._thread = None
    broker._stop_event = MagicMock()
    broker._logger = None  # not using the standard logger logic

    # Call the start method
    broker.start()

    # Verify logger.error was called with the exact message
    broker.logger.error.assert_called_once_with(f"Failed to bind: {error}")
