import asyncio
import json
import pytest
from unittest.mock import MagicMock

# Attempt to import websockets for client testing
try:
    import websockets
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False

from sagittarius_engine import App
from sagittarius_engine.infrastructure import StdLibContainer, MemoryEventBus
from sagittarius_engine.extensions.audit.audit_service import AuditService
from sagittarius_engine.extensions.audit.events import SystemStateChangedEvent

@pytest.mark.asyncio
async def test_audit_broadcaster_sends_updates():
    """
    [Integration Test]
    Tests that the AuditService WebSocket Broadcaster pushes initial state, 
    and also pushes updates when subscribed events occur on the EventBus.
    """
    if not WEBSOCKETS_AVAILABLE:
        pytest.skip("websockets library is not installed.")

    # 1. Setup Backend Engine
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    App(container, event_bus)

    # Mock context since we only need event_bus for this test
    context = MagicMock()
    context.event_bus = event_bus
    context.tasks = MagicMock()
    context.extension_manager = MagicMock()
    context.hosted_services = MagicMock()

    # Create and start AuditService on a test port
    test_port = 9998
    audit_service = AuditService(context, port=test_port)
    
    # Mock _get_full_state to avoid JSON serialization errors with MagicMock
    audit_service._get_full_state = MagicMock(return_value={"uptime": 123.4, "status": "mocked"})
    audit_service.broadcaster.on_new_client_callback = audit_service._get_full_state
    
    audit_service.start_server()

    # Wait a bit for the daemon thread to spin up the asyncio loop and server
    await asyncio.sleep(0.5)

    # 2. Setup Client (simulating the Dashboard)
    received_messages = []
    
    # We use websockets.connect as a client to verify the behavior
    # For websockets 14.0+, we can use websockets.asyncio.client.connect if needed,
    # but the standard websockets.connect works in both legacy and new for simple tests.
    try:
        from websockets.asyncio.client import connect
        async with connect(f"ws://127.0.0.1:{test_port}") as websocket:
            # 3. Verify Initial State
            # The server pushes 'initial_state' immediately upon connection
            initial_message = await websocket.recv()
            initial_data = json.loads(initial_message)
            received_messages.append(initial_data)
            
            assert initial_data["event"] == "initial_state"
            assert "uptime" in initial_data["data"]

            # 4. Trigger an event that AuditService listens to
            # This simulates a system action that triggers an update
            event_bus.emit("SystemStateChangedEvent", SystemStateChangedEvent(state_snapshot={"test": "data"}))

            # 5. Verify State Update is pushed
            update_message = await asyncio.wait_for(websocket.recv(), timeout=2.0)
            update_data = json.loads(update_message)
            received_messages.append(update_data)
            
            assert update_data["event"] == "state_update"
            assert "uptime" in update_data["data"]
            
    except ImportError:
        # Fallback for older websockets API
        async with websockets.connect(f"ws://127.0.0.1:{test_port}") as websocket:
            initial_message = await websocket.recv()
            initial_data = json.loads(initial_message)
            received_messages.append(initial_data)
            
            assert initial_data["event"] == "initial_state"

            event_bus.emit("SystemStateChangedEvent", SystemStateChangedEvent(state_snapshot={"test": "data"}))

            update_message = await asyncio.wait_for(websocket.recv(), timeout=2.0)
            update_data = json.loads(update_message)
            received_messages.append(update_data)
            
            assert update_data["event"] == "state_update"
            
    finally:
        # Stop the backend server
        audit_service.stop_server()

    # We should have received exactly 2 messages
    assert len(received_messages) == 2
