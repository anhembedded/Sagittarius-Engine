> Applies to Sagittarius Engine v1.x

# EngineContext

The `EngineContext` class acts as the shared composition root of the Sagittarius Engine. It maintains references to every internal subsystem, the dependency injection container, the event bus, and the extension manager.

## Purpose

`EngineContext` is passed to extensions during their lifecycle methods (`initialize`, `start`, `stop`, `dispose`) so they can resolve dependencies or interact with the engine.

## Related APIs

- **[App](app.md)**: Exposes the primary facade.
- **[IExtension](extension.md)**: Interacts with the context.
- **[Dispatcher](dispatcher.md)**: Dispatches requests using container services.

---

## Architecture Diagrams

### Composition Flowchart

The following diagram shows the subsystems composed and managed by `EngineContext`:

```mermaid
flowchart TD
    EngineContext[EngineContext] --> Core[Core Subsystems]
    EngineContext --> Infrastructure[Runtime Infrastructure]
    EngineContext --> Shared[Shared Abstractions]

    subgraph Core [Core Subsystems]
        Dispatcher[Dispatcher]
        Bootstrap[Bootstrap]
        Lifecycle[Lifecycle]
        ExtensionManager[Extension Manager]
        ModuleLoader[Module Loader]
    end

    subgraph Infrastructure [Runtime Infrastructure]
        AsyncRuntime[Async Runtime]
        TaskManager[Task Manager]
        Scheduler[Scheduler]
        HostedServices[Hosted Service Manager]
    end

    subgraph Shared [Shared Abstractions]
        Container[IContainer]
        EventBus[IEventBus]
    end
```

### Lifecycle Flow Diagrams

#### 1. Boot Sequence

The chronological runtime flow of booting the application via `EngineContext` subsystems:

```mermaid
sequenceDiagram
    participant App
    participant Bootstrap
    participant Lifecycle
    participant AsyncRuntime
    participant ModuleLoader
    participant ExtensionManager
    participant HostedServices
    participant Scheduler
    participant EventBus

    App->>Bootstrap: boot(auto_discover)
    activate Bootstrap
    Bootstrap->>Lifecycle: set_booting()
    Bootstrap->>AsyncRuntime: start()
    
    Note over Bootstrap,ModuleLoader: If auto_discover package is provided
    Bootstrap->>ModuleLoader: discover_and_load(package)
    
    Bootstrap->>ExtensionManager: initialize_and_start()
    Bootstrap->>HostedServices: start()
    Bootstrap->>Scheduler: start()
    Bootstrap->>Lifecycle: set_booted()
    
    Bootstrap->>EventBus: emit("app.booted", App)
    deactivate Bootstrap
```

#### 2. Shutdown Sequence

The chronological runtime flow of stopping the application gracefully:

```mermaid
sequenceDiagram
    participant App
    participant Lifecycle
    participant Scheduler
    participant HostedServices
    participant ExtensionManager
    participant TaskManager
    participant AsyncRuntime

    App->>Lifecycle: set_stopping()
    
    App->>Scheduler: stop()
    App->>HostedServices: stop()
    App->>ExtensionManager: stop_and_dispose()
    App->>TaskManager: shutdown()
    App->>AsyncRuntime: stop()
    
    App->>Lifecycle: set_stopped()
```

### Class Diagrams

#### High-Level Class Dependency Diagram

```mermaid
classDiagram
    class EngineContext
    class App
    class IContainer {
        <<interface>>
    }
    class IEventBus {
        <<interface>>
    }
    class Subsystems {
        <<conceptual group>>
    }

    EngineContext --> App : references
    EngineContext --> IContainer : references
    EngineContext --> IEventBus : references
    EngineContext *-- Subsystems : composes & coordinates
```

#### Detailed Class Diagram

```mermaid
classDiagram
    class EngineContext {
        +app: App
        +container: IContainer
        +event_bus: IEventBus
        +middleware_pipeline: MiddlewarePipeline
        +extension_manager: ExtensionManager
        +lifecycle: EngineLifecycle
        +module_loader: ModuleLoader
        +bootstrap: Bootstrap
        +dispatcher: Dispatcher
        +async_runtime: AsyncRuntime
        +tasks: TaskManager
        +scheduler: Scheduler
        +hosted_services: HostedServiceManager
        +modules: list
        +logger: ILogger
        +config: IConfig
    }

    class App {
        +context: EngineContext
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

    class Bootstrap {
        +context: EngineContext
        +boot(auto_discover: str) void
    }

    class Dispatcher {
        +context: EngineContext
        +dispatch(handler_class: type, input_dto: Any) Any
    }

    class EngineLifecycle {
        +context: EngineContext
        +state: str
        +set_booting() void
        +set_booted() void
        +set_stopping() void
        +set_stopped() void
    }

    EngineContext --> App : references
    EngineContext --> IContainer : references
    EngineContext --> IEventBus : references
    EngineContext *-- Bootstrap : composes & invokes
    EngineContext *-- Dispatcher : composes & invokes
    EngineContext *-- EngineLifecycle : composes & updates
```

---

## Reference

::: sagittarius_engine.kernel.context.EngineContext

---

> [Found an issue? Edit this page on GitHub.](https://github.com/anhembedded/Sagittarius-Engine/edit/main/docs/api/engine_context.md)

