# Queue Worker Reference Application

This reference application validates background queue worker implementations.

## Key Patterns
- **Cooperative Cancellation**: Uses a thread-safe `CancellationToken` to notify the consumer thread to exit.
- **Graceful Shutdown**: The worker stop sequence waits for the thread to complete its currently executing queue job before shutting down.
