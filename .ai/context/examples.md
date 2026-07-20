# Usage Examples

This document serves as the single source of truth for all reference applications in the `examples/` directory.
It ensures that tutorials, concepts, and guides remain synchronized with the provided code examples.

## Catalog

### 1. Desktop Application

- **Directory**: `examples/desktop`
- **Purpose**: Demonstrates how to integrate Sagittarius Engine with event-driven, thread-safe UI updates (PySide6). Shows proper shutdown sequences and bridging events.
- **Difficulty**: Intermediate
- **Related Tutorial**: [Desktop App Tutorial](../docs/tutorials/desktop_app.md)
- **Related Concepts**: Extension System, Engine Lifecycle
- **Related Runtime Guide**: Hosted Services, Dispatcher
- **Related API**: `IHostedService`, `IEventBus`, `Extension`

### 2. Worker Service

- **Directory**: `examples/worker`
- **Purpose**: Demonstrates a background queue consumer executing tasks with cooperative cancellation.
- **Difficulty**: Beginner
- **Related Tutorial**: [Worker Service Tutorial](../docs/tutorials/worker_service.md)
- **Related Concepts**: Task Processing
- **Related Runtime Guide**: TaskManager, CancellationToken
- **Related API**: `ITaskManager`, `CancellationToken`

### 3. Trading Bot

- **Directory**: `examples/trading_bot`
- **Purpose**: Demonstrates building long-running strategy loops using `HostedService`, `TaskManager`, and `Scheduler`.
- **Difficulty**: Advanced
- **Related Tutorial**: [Trading Bot Tutorial](../docs/tutorials/trading_bot.md)
- **Related Concepts**: Long-running loops
- **Related Runtime Guide**: Scheduler, Async Runtime
- **Related API**: `IScheduler`, `IHostedService`

### 4. WebSocket Client

- **Directory**: `examples/websocket`
- **Purpose**: Demonstrates asynchronous client connections, backoff reconnects, and heartbeats via the Async Runtime.
- **Difficulty**: Intermediate
- **Related Tutorial**: [WebSocket Client Tutorial](../docs/tutorials/websocket_client.md)
- **Related Concepts**: Asynchronous networking
- **Related Runtime Guide**: Async Runtime
- **Related API**: `IAsyncRuntime`

### 5. Plugin System

- **Directory**: `examples/plugin_system`
- **Purpose**: Demonstrates dynamic Extension loading, Extension discovery, Extension dependency graph, and Extension activation.
- **Difficulty**: Advanced
- **Related Tutorial**: [Plugin System Tutorial](../docs/tutorials/plugin_system.md)
- **Related Concepts**: Extension System
- **Related Runtime Guide**: Application Lifecycle
- **Related API**: `IExtension`, `ExtensionContext`

### 6. REST API (No Tutorial Yet)

- **Directory**: `examples/rest_api`
- **Purpose**: Simple HTTP server using the DI Container and Dispatcher.
- **Difficulty**: Beginner
- **Related Tutorial**: N/A
- **Related Concepts**: DI Container, Web
- **Related Runtime Guide**: N/A
- **Related API**: `IContainer`

