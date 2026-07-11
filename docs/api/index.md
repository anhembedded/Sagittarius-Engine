> Applies to Sagittarius Engine v1.x

# API Reference Overview

Welcome to the API Reference for Sagittarius Engine. This section provides detailed technical documentation for all public classes, interfaces, and functions.

## Public API Scope

Sagittarius Engine exposes a stable public API surface that covers application lifecycle management, dependency injection, unified request dispatching, event-driven communication, and runtime capabilities (hosted services, task management, scheduling).

## Core Classes & Interfaces

- **[App](app.md)**: Main host entry point and orchestrator.
- **[EngineContext](engine_context.md)**: Shared runtime service registry and composition root.
- **[Dispatcher](dispatcher.md)**: Unified command and query request dispatcher.
- **[IEventBus](event_bus.md)**: Pub/Sub event bus interface for decoupled communication.
- **[IExtension & ExtensionDescriptor](extension.md)**: Interfaces for writing plugins.
- **[IHostedService](hosted_service.md)**: Interface for long-running background tasks.
- **[Scheduler](scheduler.md)**: Time-based cron and interval scheduler.
- **[TaskManager](task_manager.md)**: Utility for spawning and monitoring background tasks.
- **[CancellationToken](cancellation_token.md)**: Cooperative cancellation model.

---

> [Found an issue? Edit this page on GitHub.](https://github.com/your-repo/edit/main/docs/api/index.md)
