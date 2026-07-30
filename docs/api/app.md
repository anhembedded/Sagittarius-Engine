> Applies to Sagittarius Engine v1.x

# App

The `App` class is the primary entry point and orchestrator for the Sagittarius Engine. It initializes the dependency injection container, the event bus, and coordinates the boot and shutdown phases of the application host.

## Purpose

Use `App` to configure your composition root, load extensions, attach middleware pipelines, and trigger the boot sequence.

## Related APIs

- **[EngineContext](engine_context.md)**: Coordinates operations under the hood.
- **[IEventBus](event_bus.md)**: Manages communication between components.
- **[IExtension](extension.md)**: Extend App capabilities.

---

## Architecture Diagrams

### 1. Runtime Lifecycle State Diagram

The following diagram illustrates the application states managed by the engine's lifecycle:

```mermaid
stateDiagram-v2
    [*] --> Stopped
    Stopped --> Booting : boot()
    Booting --> Booted : startup complete
    Booted --> Stopping : stop()
    Stopping --> Stopped : shutdown complete
    Stopped --> [*]
```

### 2. Request Execution Sequence Diagram

The chronological runtime sequence of dispatching a command or query request:

```mermaid
sequenceDiagram
    participant Client as Application Client
    participant App as App Facade
    participant Dispatcher as Dispatcher
    participant Container as DI Container
    participant Pipeline as Middleware Pipeline
    participant Handler as Command/Query Handler

    Client->>App: dispatch(HandlerClass, DTO)
    activate App
    App->>Dispatcher: dispatch(HandlerClass, DTO)
    activate Dispatcher
    
    Dispatcher->>Container: resolve(HandlerClass)
    Container-->>Dispatcher: Handler Instance
    
    Dispatcher->>Pipeline: execute(Handler, DTO, final_callback)
    activate Pipeline
    
    Note over Pipeline: Runs through all registered IMiddleware
    
    Pipeline->>Handler: execute(DTO)
    activate Handler
    Handler-->>Pipeline: Result
    deactivate Handler
    
    Pipeline-->>Dispatcher: Result
    deactivate Pipeline
    
    Dispatcher-->>App: Result
    deactivate Dispatcher
    App-->>Client: Result
    deactivate App
```

### 3. Core Interface Relationships Flowchart

The following diagram maps how the `App` facade coordinates with other engine interfaces:

```mermaid
flowchart LR
    ClientApp[Client App] --> App[App Facade]
    App --> Container[DI Container]
    App --> EventBus[EventBus]
    App --> Dispatcher[Dispatcher]
    App --> MiddlewarePipeline[Middleware Pipeline]

    Dispatcher --> Container
    Dispatcher --> MiddlewarePipeline
```

### 4. Class Diagrams

#### High-Level Class Dependency Diagram

```mermaid
classDiagram
    class App
    class EngineContext
    class IContainer {
        <<interface>>
    }
    class IEventBus {
        <<interface>>
    }
    class IMiddleware {
        <<interface>>
    }

    App *-- EngineContext : delegates state & orchestration
    App ..> IContainer : receives & uses
    App ..> IEventBus : receives & uses
    App ..> IMiddleware : registers
```

#### Detailed Class Diagram

```mermaid
classDiagram
    class App {
        +EngineContext context
        +container: IContainer
        +event_bus: IEventBus
        +modules: list
        +pipeline: Any
        +lifecycle: Any
        +use(extension_or_module: Any) void
        +use_middleware(middleware_instance: IMiddleware) void
        +boot(auto_discover: str) void
        +dispatch(handler_class: type, input_dto: Any) Any
        +stop() void
    }

    class EngineContext {
        +App app
        +IContainer container
        +IEventBus event_bus
        +middleware_pipeline: MiddlewarePipeline
        +extension_manager: ExtensionManager
        +bootstrap: Bootstrap
        +dispatcher: Dispatcher
        +lifecycle: RuntimeLifecycle
    }

    class IContainer {
        <<interface>>
        +bind(interface, concrete)
        +singleton(interface, instance_or_factory)
        +resolve(interface_or_type)
    }

    class IEventBus {
        <<interface>>
        +on(event_name, handler)
        +emit(event_name, event)
    }

    class IMiddleware {
        <<interface>>
        +process(request, next_call)
    }

    App *-- EngineContext : delegates operations
    App ..> IContainer : access & resolve
    App ..> IEventBus : event dispatching
    App ..> IMiddleware : pipeline extension
```

---


## Reference

::: sagittarius_engine.kernel.app.App

---

> [Found an issue? Edit this page on GitHub.](https://github.com/anhembedded/Sagittarius-Engine/edit/main/docs/api/app.md)
