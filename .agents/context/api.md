# API & Interface Contracts

The Sagittarius Engine uses explicit Abstractions (Interfaces) for decoupled architecture. Developers should depend on `sagittarius_engine.interfaces.*` rather than concrete implementations.

## Primary Kernel APIs

### `App` Facade
The main entry point for the application.
- **`app.use(module_or_extension)`**: Registers a module or extension.
- **`app.boot(auto_discover=True)`**: Boots the container, runtime, and extensions.
- **`app.dispatch(CommandClass, input_dto)`**: Resolves a handler mapped to `CommandClass` via the DI container and executes it, passing `input_dto`.
- **`app.stop()`**: Initiates a graceful shutdown of all tasks and services.

### `IEngineContext`
Passed to modules and services, providing access to:
- **`context.container`**: The Dependency Injection container (`IContainer`).
- **`context.event_bus`**: The Event Bus (`IEventBus`) to emit/listen to domain and system events.
- **`context.tasks`**: The Task Manager (`ITaskManager`) for spawning background workers.

## Key Interfaces

- **`IModule`**: Must implement `register(app)` and `boot(app)`.
- **`IHostedService`**: Must implement `start(context)` and `stop(context)`.
- **`IEventBus`**: `on(event, callback)` and `emit(event, data)`.
- **`IContainer`**: `bind(interface, concrete)`, `singleton(interface, instance)`, `resolve(interface)`.
