# WebSocket Client Reference Application

This reference application validates asynchronous event loop execution, heartbeat, and reconnection logic.

## Key Patterns
- **Async loops inside Sync Engine**: Spawns coroutine connection loops on the background thread loop safely.
- **Auto-reconnect with Backoff**: Implements exponential backoff when a connection drop is encountered.
- **Heartbeat Coordination**: Spawns a sub-coroutine for periodic ping messaging that gets canceled cleanly when the main socket listener loop disconnects.
