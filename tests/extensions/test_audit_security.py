import asyncio
import pytest
from unittest.mock import MagicMock
import socket
from websockets.exceptions import ConnectionClosedError, ConnectionClosed

try:
    import websockets
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False

from sagittarius_engine.extensions.audit.audit_service import AuditService

@pytest.mark.asyncio
async def test_audit_websocket_rejects_missing_or_invalid_token():
    """
    [Integration Test]
    Tests that the AuditService WebSocket Broadcaster rejects connections without a valid token.
    """
    if not WEBSOCKETS_AVAILABLE:
        pytest.skip("websockets library is not installed.")

    # Setup Backend Engine
    context = MagicMock()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    test_port = s.getsockname()[1]
    s.close()

    audit_service = AuditService(context, port=test_port, token="SECRET_TOKEN_123")
    audit_service._get_full_state = MagicMock(return_value={})
    audit_service.broadcaster.on_new_client_callback = audit_service._get_full_state

    audit_service.start_server()
    await asyncio.sleep(0.5)

    try:
        try:
            from websockets.asyncio.client import connect
        except ImportError:
            connect = websockets.connect

        # 1. Test missing token
        with pytest.raises((ConnectionClosedError, ConnectionClosed)):
            async with connect(f"ws://127.0.0.1:{test_port}") as websocket:
                await websocket.recv()

        # 2. Test invalid token
        with pytest.raises((ConnectionClosedError, ConnectionClosed)):
            async with connect(f"ws://127.0.0.1:{test_port}/?token=WRONG_TOKEN") as websocket:
                await websocket.recv()

        # 3. Test valid token
        async with connect(f"ws://127.0.0.1:{test_port}/?token=SECRET_TOKEN_123") as websocket:
            msg = await websocket.recv()
            assert msg is not None

    finally:
        audit_service.stop_server()
