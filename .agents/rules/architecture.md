---
trigger: model_decision
---

# Rules: Architecture

Module boundaries, dependency guidelines, and layout rules.

## IEngineContext — God Object Prevention

`IEngineContext` must ONLY be used during the engine's Bootstrap and Extension lifecycle phase.

### ✅ Valid Usage
- Inside `IExtension.register()`, `boot()`, `shutdown()`, `boot_async()`, `shutdown_async()`.
- Inside `IHostedService.start()` and `stop()`.
- Inside Kernel orchestrators: `Bootstrap`, `AppRunner`, `ExtensionManager`.

### ❌ Invalid Usage
- Inside `domain/` layer (entities, value objects, domain services).
- Inside `application/` layer (use cases, command/query handlers, application services).
- As a constructor parameter (`__init__`) of any non-extension class.

### Correct Pattern
Register dependencies in `IExtension.register()` using `context.container`, then inject them
into use cases / handlers via the DI Container — never pass `IEngineContext` itself:

```python
# ✅ Correct
class MyExtension(IExtension):
    def register(self, context: IEngineContext) -> None:
        context.container.singleton(IMyRepo, ConcreteRepo)

class MyUseCase:  # Gets IMyRepo injected by container — NOT IEngineContext
    def __init__(self, repo: IMyRepo) -> None:
        self._repo = repo

# ❌ Wrong
class MyUseCase:
    def __init__(self, context: IEngineContext) -> None:  # God Object anti-pattern!
        self._context = context
```

## Module Boundaries

- `sagittarius_engine/interfaces/` — Pure abstractions only. No concrete imports.
- `sagittarius_engine/kernel/` — Internal orchestration. Uses `IKernelContext` not `IEngineContext`.
- `sagittarius_engine/extensions/` — Feature extensions. Depend on `IEngineContext` only.
- `sagittarius_engine/infrastructure/` — Adapters and implementations. No domain imports.
