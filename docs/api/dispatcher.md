> Applies to Sagittarius Engine v1.x

# Dispatcher

The `Dispatcher` is responsible for routing command and query requests through the application's registered middleware pipeline before invoking the final request handler.

## Purpose

Use the `Dispatcher` (via `App.dispatch`) to execute commands and queries. This decouples request senders from their handlers.

## Related APIs

- **[App](app.md)**: Exposes the `dispatch` method directly.
- **[EngineContext](engine_context.md)**: Owns the dispatcher instance.

---

## Architecture Diagrams

### 1. Dispatch Workflow Flowchart

The following diagram shows how a command or query request routes through the `Dispatcher`:

```mermaid
flowchart LR
    Request[Command/Query DTO] --> Dispatcher[Dispatcher]
    Dispatcher --> Container[Container DI]
    Container --> HandlerInstance[Resolved Handler]
    Dispatcher --> Pipeline[Middleware Pipeline]
    Pipeline --> HandlerInstance
    HandlerInstance --> Result[Execution Result]
```

### 2. Request Execution Sequence Diagram

The step-by-step sequence of dispatching a command or query:

```mermaid
sequenceDiagram
    participant App
    participant Dispatcher
    participant Container as DI Container
    participant Pipeline as Middleware Pipeline
    participant Handler

    App->>Dispatcher: dispatch(handler_class, DTO)
    activate Dispatcher
    
    Dispatcher->>Container: resolve(handler_class)
    Container-->>Dispatcher: handler instance
    
    Dispatcher->>Pipeline: execute(handler, DTO, final_callback)
    activate Pipeline
    
    Note over Pipeline: Runs through all registered middleware
    
    Pipeline->>Handler: execute(DTO)
    activate Handler
    Handler-->>Pipeline: Result
    deactivate Handler
    
    Pipeline-->>Dispatcher: Result
    deactivate Pipeline
    
    Dispatcher-->>App: Result
    deactivate Dispatcher
```

### 3. Class Diagrams

#### High-Level Class Dependency Diagram

```mermaid
classDiagram
    class Dispatcher
    class EngineContext
    class IContainer {
        <<interface>>
    }
    class MiddlewarePipeline

    Dispatcher --> EngineContext : references
    Dispatcher ..> IContainer : resolves handlers
    Dispatcher ..> MiddlewarePipeline : executes pipeline
```

#### Detailed Class Diagram

```mermaid
classDiagram
    class Dispatcher {
        +context: EngineContext
        +dispatch(handler_class: type, input_dto: Any) Any
    }

    class EngineContext {
        +container: IContainer
        +middleware_pipeline: MiddlewarePipeline
    }

    class IContainer {
        <<interface>>
        +resolve(interface_or_type) Any
    }

    class MiddlewarePipeline {
        +execute(handler, dto, final_callback) Any
    }

    class Handler {
        <<interface>>
        +execute(dto) Any
    }

    Dispatcher --> EngineContext
    Dispatcher ..> IContainer
    Dispatcher ..> MiddlewarePipeline
    Dispatcher ..> Handler : resolves & passes
```

---

## Reference

::: sagittarius_engine.kernel.dispatcher.Dispatcher

---

> [Found an issue? Edit this page on GitHub.](https://github.com/your-repo/edit/main/docs/api/dispatcher.md)
