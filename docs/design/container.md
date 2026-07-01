---
type: design_doc
tags: [sagittarius, container]
language: python
---

# Container

## Overview
The `IContainer` interface and its implementation `StdLibContainer` form the dependency injection framework for Sagittarius. The container is responsible for managing the instantiation and distribution of class dependencies, adhering to the Inversion of Control (IoC) principle.

## Problem Statement
In Clean Architecture, high-level policies (Domain/App layers) must not depend directly on low-level details (Infrastructure layers). Instead, they depend on abstractions (Ports/Interfaces). We need a mechanism to wire these abstractions to their concrete implementations at runtime so that the application components are completely decoupled and easily testable.

## Proposed Solution
The Container provides a central registry where interfaces can be bound to implementations (`bind()`) or singletons (`singleton()`). When the framework or a module requests an instance (`resolve()`), the container uses Python's standard `inspect` library to read type hints on the constructor, automatically recursively resolving and injecting all required dependencies.

## Core API / Interface

### `interface IContainer` (in `src/interfaces/i_container.py`)
Abstract base class representing a Dependency Injection Container.

- `def bind(self, abstract: type, concrete: type) -> None`: Binds an Interface to a specific Implementation (transient lifecycle - new instance on every resolve).
- `def singleton(self, abstract: type, instance_or_factory: Union[Any, Callable]) -> None`: Registers a Singleton instance or a factory function. The instance is created once and reused.
- `def resolve(self, abstract: type[T]) -> T`: Resolves and returns an instance of the requested type.

### `class StdLibContainer(IContainer)` (in `src/infra/std_container.py`)
Standard implementation utilizing Python's `inspect` module.

- `def __init__(self) -> None`: Initializes the binding, factory, and instance registries.
- `def bind(self, abstract: type, concrete: type) -> None`: Registers a transient mapping.
- `def singleton(self, abstract: type, instance_or_factory: Union[Any, Callable]) -> None`: Registers a singleton instance or factory function.
- `def resolve(self, abstract: type[T]) -> T`: Recursively resolves and retrieves an instance, reading type hints via `inspect.signature`.

## Dependencies
- Internal: `IContainer`, `DependencyResolutionError`
- External: Standard libraries (`inspect`, `typing`)

## How to Use / Examples

```python
from src.interfaces import IContainer
from src.infra.std_container import StdLibContainer

# Assume interfaces IUserRepository, IEventBus exist
# Assume implementations PostgresUserRepository, MemoryEventBus exist

container = StdLibContainer()

# 1. Register a Singleton (A single shared instance)
container.singleton(IEventBus, MemoryEventBus())

# 2. Register a standard Binding (A new instance is created on each resolve)
container.bind(IUserRepository, PostgresUserRepository)

# 3. Use a factory function if initialization is complex
def make_db(container: IContainer):
    return DatabaseConnection(host="localhost")
container.singleton(DatabaseConnection, make_db)

# 4. Resolve (Automatic dependency injection)
# The container will automatically fetch required dependencies based on type hints.
repo = container.resolve(IUserRepository)
```

## Implementation Notes
- **Type Hinting Requirement**: All constructor parameters (`__init__`) must have explicit type hints for automatic resolution to work. If a type hint is missing, a `DependencyResolutionError` is raised.
- **Fallbacks**: If resolution of a dependency fails but the parameter has a default value (e.g., `Optional`), the container will use the default value.
- **Abstract Classes**: Trying to resolve an abstract class that has not been explicitly bound to a concrete implementation will raise a `DependencyResolutionError`.
- Factory functions passed to `singleton` are evaluated lazily on the first call to `resolve`.

## Related Documents
- `app_kernel.md`
- `exceptions.md`
