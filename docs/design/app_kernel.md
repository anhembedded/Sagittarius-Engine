---
type: design_doc
tags: [sagittarius, app_kernel]
language: python
---

# App Kernel

## Overview
The `App` class is the heart of the Sagittarius Framework (Application Facade). It acts as the Orchestrator, connecting the Container, EventBus, Modules, and Middlewares together. It manages the lifecycle of the application and handles the execution of commands and queries.

## Problem Statement
A Clean Architecture application needs a central composition root to assemble dependencies, route execution flow through pipelines, manage application lifecycle phases (register/boot), and provide a unified entry point. Without it, the application's bootstrapping and operational mechanics would be scattered and coupled.

## Proposed Solution
The App Kernel provides the `App` class which manages:
- **Dependency Injection**: Delegates to `IContainer`.
- **Event Driven Communication**: Integrates with `IEventBus`.
- **Modularity**: Supports manual registration (`use()`) and automatic discovery (`ModuleAutoDiscovery`) of `IModule` components.
- **Request Lifecycle**: Commands and Queries are pushed through the `MiddlewarePipeline` using an Onion architecture pattern before hitting the final execution handler.

## Core API / Interface

### `class App`
The main application facade.

- `def __init__(self, container: IContainer, event_bus: IEventBus) -> None`: Initializes the application with core ports.
- `def use(self, module: IModule) -> None`: Manually adds a Module and calls its `register` method immediately.
- `def use_middleware(self, middleware_instance: IMiddleware) -> None`: Registers a Middleware to the application pipeline.
- `def boot(self, auto_discover: Optional[str]=None) -> None`: Boots the application, auto-discovers modules if specified, calls `boot` on all modules, and emits the `app.booted` event.
- `def execute(self, command_class: type[ICommand], input_dto: Any=None) -> Any`: Executes a Command through the Middleware Pipeline.
- `def query(self, query_class: type[IQuery], input_dto: Any=None) -> Any`: Executes a Query through the Middleware Pipeline.

### `class MiddlewarePipeline`
Manages the middleware chain.

- `def add(self, middleware: IMiddleware) -> None`: Appends a middleware to the end of the chain.
- `def execute(self, cmd_or_query: Any, dto: Any, final_handler: Callable[[], Any]) -> Any`: Executes the entire middleware chain using an onion approach.

### `class ModuleAutoDiscovery`
Auto-discovers and loads modules dynamically.

- `def discover(modules_package_str_path: str, app: 'App') -> None`: Scans a specified package, finding and registering implementations of `IModule`.

## Dependencies
- Internal: `IModule`, `IContainer`, `IEventBus`, `IMiddleware`, `ICommand`, `IQuery`, `ILogger`, `BaseModule`, `ModuleRegistrationError`, `DependencyResolutionError`
- External: Standard libraries (`inspect`, `pkgutil`, `importlib`, `abc`, `typing`)

## How to Use / Examples

```python
from src.app_kernel import App
from src.infra.std_container import StdLibContainer
from src.infra.memory_event_bus import MemoryEventBus

# Initialize core dependencies
container = StdLibContainer()
event_bus = MemoryEventBus()

# Create application instance
app = App(container, event_bus)

# Boot and auto-discover modules
app.boot(auto_discover="src.modules")

# Execute a command
# app.execute(CreateUserCommand, CreateUserDTO(name="Alice"))
```

## Implementation Notes
- Auto-discovery gracefully skips un-importable modules or non-modules.
- Middlewares wrap each other sequentially. A failure in one middleware halts the pipeline execution unless properly handled.
- The `app.booted` event is emitted synchronously after booting all modules.

## Related Documents
- `container.md`
- `event_bus.md`
- `modules.md`
- `middleware.md`
