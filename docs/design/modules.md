---
type: design_doc
tags: [sagittarius, module]
language: python
---

# Modules

## Overview
Modules represent isolated, independent organizational units within the Sagittarius Framework (akin to plugins). They structure the codebase logically, grouping related controllers, services, repositories, commands, and queries together.

## Problem Statement
In scaling Clean Architecture applications, dropping all dependencies and event subscriptions into a single `main.py` creates a bloated composition root. Applications need a way to modularize features so they can cleanly register their own dependencies and bootstrap processes without interfering with others.

## Proposed Solution
Sagittarius defines the `IModule` interface. Modules are loaded into the application (either manually via `App.use()` or via `ModuleAutoDiscovery`). The module lifecycle consists of two phases:
1. **Registration (`register`)**: Used strictly to bind dependencies, commands, and queries into the framework's DI Container.
2. **Bootstrapping (`boot`)**: Called after *all* modules have successfully registered. Used to establish database connections, subscribe to events, and start background workers.

To reduce boilerplate, developers can inherit from `BaseModule`, which provides no-op implementations of `register` and `boot`.

## Core API / Interface

### `interface IModule` (in `src/interfaces/i_module.py`)
Abstract base class representing an application Module.

- `def register(self, app: 'App') -> None`: Called first when the module is added. Used to bind dependencies into the `IContainer`.
- `def boot(self, app: 'App') -> None`: Called after all modules are registered. Used for initialization tasks and subscribing to the `IEventBus`.

### `class BaseModule(IModule)` (in `src/base_module.py`)
A convenience base class that implements empty methods (pass) for `register` and `boot`.

- `def register(self, app: 'App') -> None`: Default pass.
- `def boot(self, app: 'App') -> None`: Default pass.

## Dependencies
- Internal: `App` (passed into methods, typing forward reference `'App'`)

## How to Use / Examples

```python
from src.base_module import BaseModule

class DatabaseModule(BaseModule):
    """
    Example Database Module that registers a DB connection.
    """

    def register(self, app: 'App') -> None:
        # Register dependencies in the container during the register phase
        app.container.singleton('DatabaseConnection', PostgresDB("localhost"))
        app.container.bind('IUserRepository', PostgresUserRepository)

    def boot(self, app: 'App') -> None:
        # Subscribe to events or run startup logic in the boot phase
        db = app.container.resolve('DatabaseConnection')
        db.connect()

        # Log successful connection via event bus
        app.event_bus.on('app.booted', lambda data: print("DB Module ready!"))
```

## Implementation Notes
- **Two-Phase Initialization**: It's crucial to follow the two-phase rule. Cross-module dependency resolution should only happen inside `boot()`. Resolving dependencies inside `register()` might result in a `DependencyResolutionError` because other modules may not have registered their components yet.
- Modules can be single Python files containing an `IModule` class, or directories with an `__init__.py` file exposing an `IModule` class. This allows seamless integration with `ModuleAutoDiscovery` in `app_kernel.py`.

## Related Documents
- `app_kernel.md`
- `container.md`
