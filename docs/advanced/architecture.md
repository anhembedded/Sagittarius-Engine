> Applies to Sagittarius Engine v1.x

# Advanced Architecture

## Overview

The Sagittarius Engine architecture is designed to orchestrate complex background services, extensions, and lifecycle events under a unified framework. This document breaks down the structural layers of a Sagittarius application to help architects and maintainers understand ownership and collaboration.

## Why

As applications scale to include dozens of extensions, multiple background tasks, and complex domain logic, understanding *where* code belongs is critical. A clear architectural boundary prevents "God Objects" and ensures that lifecycle events are handled predictably.

## When to Use

Use this architectural knowledge when:
- Designing custom extensions that interact with core runtime features.
- Debugging memory leaks or lifecycle deadlocks.
- Explaining the system boundary to new team members.

## When NOT to Use

Do NOT rely on this document for:
- API references for specific classes (see the API Reference instead).
- Domain-Driven Design (DDD) rules for your specific business logic.

## Architecture

```mermaid
flowchart TB
    subgraph Application Boundary
        AppHost[Application]
        App[App Instance]
    end

    subgraph Core
        Kernel[Kernel]
        EngineContext[EngineContext]
        Runtime[Runtime Environment]
    end

    subgraph Extensions Layer
        Ext1[Extension A]
        Ext2[Extension B]
    end

    subgraph Infrastructure Services
        HSM[HostedServiceManager]
        TM[TaskManager]
        Sched[Scheduler]
        AR[AsyncRuntime]
        Disp[Dispatcher]
    end

    AppHost -->|Creates| App
    App -->|Owns| Kernel
    Kernel -->|Owns| Runtime
    Kernel -->|Initializes| Extensions Layer
    Runtime -->|Manages| Infrastructure Services
    App -->|Exposes| EngineContext
    EngineContext -->|Provides Access To| Infrastructure Services
```

## How it Works

The architecture is strictly layered to enforce ownership and lifecycle guarantees:

1. **Application / App Host**: The user-defined entry point (e.g., `main.py`). It instantiates the `App`, configures dependency injection, registers extensions, and calls `app.boot()`.
2. **App Instance**: The highest-level framework object. It acts as the facade for the Kernel and holds the `EngineContext`.
3. **Kernel**: Responsible for resolving the dependency graph and managing the state machine of the boot/shutdown sequence.
4. **Runtime Environment**: The active execution space that owns the event loops, thread pools, and long-running services.
5. **EngineContext**: A read-only data structure passed to extensions and services, providing safe access to Infrastructure Services (like the TaskManager or Dispatcher).
6. **Extensions**: Isolated, modular components that register types with the DI container and boot up background processes.
7. **Infrastructure Services**: The engine's built-in managers (HostedServiceManager, TaskManager, Scheduler, AsyncRuntime, Dispatcher) that provide low-level primitives for background execution and messaging.

## Examples

### Architectural Boundary Example

```python
from sagittarius_engine import App
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus

# 1. Application Host Layer
def run_app():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    
    # 2. App Instance Layer
    app = App(container, event_bus)
    
    # 3. Kernel Layer (Extensions Registration)
    # app.use(MyExtension())
    
    # 4. Runtime Layer (Boot Sequence)
    app.boot()
    
    # Graceful exit
    app.stop()

if __name__ == "__main__":
    run_app()
```

## Design Trade-offs

*Why a unified `EngineContext` instead of injecting everything?*

Sagittarius Engine exposes an `EngineContext` that contains references to the `TaskManager`, `Scheduler`, and `Dispatcher`. While traditional Dependency Injection prefers constructor injection for every individual dependency, Sagittarius aggregates runtime primitives into the Context. This design trade-off reduces boilerplate when writing Extensions and Hosted Services, ensuring that low-level engine capabilities are always accessible without cluttering the DI container with runtime-specific singletons.

## Best Practices

- **Respect Ownership Boundaries**: Do not attempt to manually start or stop `TaskManager` threads. Allow the `Runtime` to manage infrastructure lifecycles.
- **Use the Context**: When inside an Extension's `boot()` method, interact with the engine via the provided `EngineContext` rather than importing global state.

## Anti-Patterns

### Bypassing the Kernel
Do not instantiate `Kernel` or `Runtime` directly.
```python
# ❌ Never do this
from sagittarius_engine.kernel.kernel import Kernel
k = Kernel()
k.start()
```
*Why it is discouraged:* The `App` facade guarantees that the `EngineContext` and error boundaries are configured correctly. Bypassing it leads to undefined behavior during shutdown.

## Common Mistakes

- **Treating Extensions as Domain Logic**: Extensions are infrastructure plugins. They should register your domain services, not contain the domain logic themselves.
- **Leaking Context**: Do not save the `EngineContext` into global variables.

## Related Guides

- [Performance](performance.md)
- [Best Practices](best_practices.md)

## Related API Reference

- [App](../api/app.md)
- [EngineContext](../api/engine_context.md)

## See Also

- [Concepts: Engine](../concepts/engine.md)
- [Concepts: Runtime](../concepts/runtime.md)

> [Found an issue? Edit this page on GitHub.](https://github.com/your-repo/edit/main/docs/advanced/architecture.md)
