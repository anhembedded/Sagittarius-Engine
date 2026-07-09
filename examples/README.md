# Sagittarius Engine - Reference Applications

This directory contains production-quality architectural reference implementations showcasing the capabilities of the Sagittarius Engine.

## Directory Structure

- **`trading_bot/`**: HostedServices, TaskManager, and Scheduler strategy loops.
- **`desktop_pyside/`**: Event-driven thread-safe UI update integrations.
- **`rest_api/`**: Simple HTTP server using the DI Container and Dispatcher.
- **`worker/`**: Queue consumer executing background tasks with cooperative cancellation.
- **`websocket/`**: Asynchronous client connection loop, backoff reconnects, and heartbeats.
- **`plugin_system/`**: Dynamic module loading and dependency ordering.

## Running Examples

Ensure the package dependencies are resolved:
```bash
python main.py
```
Each example's entry point is named `main.py` and can be run independently:
```bash
python examples/trading_bot/main.py
```
