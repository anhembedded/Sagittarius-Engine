> Applies to Sagittarius Engine v1.x

# Deprecated APIs

## Overview

As part of the v1.0 release, Sagittarius Engine has streamlined its internal module structure. Several interfaces and classes have been moved out of the engine core and into dedicated Extensions.

This document serves as a reference for all API endpoints that emit `DeprecationWarning`s in `v1.x` and will be permanently removed in `v2.0`.

## Architectural Deprecations

### `execute()` and `query()`

The separate routing functions `execute()` and `query()` on the `App` instance have been unified.

- **Deprecated:** `app.execute(command_class, dto)`
- **Deprecated:** `app.query(query_class, dto)`
- **Replacement:** `app.dispatch(action_class, dto)`

**Why?** Splitting them forced developers to know whether an operation was a command or a query at the invocation site, violating encapsulation. `dispatch()` routes dynamically based on the registered handler.

## Namespacing Deprecations

### CQRS Interfaces

The `ICommand` and `IQuery` interfaces are no longer considered part of the bare minimum core interfaces. They belong to the CQRS extension.

- **Deprecated:** `sagittarius_engine.interfaces.ICommand`
- **Deprecated:** `sagittarius_engine.interfaces.IQuery`
- **Replacement:** `sagittarius_engine.extensions.cqrs.ICommand`
- **Replacement:** `sagittarius_engine.extensions.cqrs.IQuery`

### Persistence Interfaces

The database adapters have been fully extracted into the Persistence extension.

- **Deprecated:** `sagittarius_engine.base.BaseRepository`
- **Replacement:** `sagittarius_engine.extensions.persistence.BaseRepository`

- **Deprecated:** `sagittarius_engine.infrastructure.persistence.ISession`
- **Replacement:** `sagittarius_engine.extensions.persistence.ISession`

- **Deprecated:** `sagittarius_engine.infrastructure.persistence.SQLAlchemySessionAdapter`
- **Replacement:** `sagittarius_engine.extensions.persistence.SQLAlchemySessionAdapter`

- **Deprecated:** `sagittarius_engine.infrastructure.persistence.DatabaseModule`
- **Replacement:** `sagittarius_engine.extensions.persistence.DatabaseExtension`

## Terminology Deprecations

### "Module" vs "Extension"

Any class ending in `*Module` (e.g., `LoggerModule`, `DatabaseModule`) is deprecated. You must use the `*Extension` equivalent (e.g., `LoggerExtension`, `DatabaseExtension`).

- **Deprecated:** `app.use(LoggerModule())`
- **Replacement:** `app.use(LoggerExtension())`

For backwards compatibility, `v1.x` allows importing `LoggerModule` as a subclass of `LoggerExtension`, but this will emit a `DeprecationWarning`.

## Ignoring Warnings Temporarily

If you are in the middle of a large migration, you can temporarily suppress deprecation warnings in Python:

```python
import warnings

# Suppress Sagittarius deprecations temporarily
warnings.filterwarnings("ignore", category=DeprecationWarning, module="sagittarius_engine.*")
```

> [!WARNING]
> Do not leave warnings suppressed in production code. All deprecated APIs listed here will be completely removed in the next major version.

## Next Steps

- Review the [Upgrading to v1.0](upgrading.md) guide to update your project step-by-step.

> [Found an issue? Edit this page on GitHub.](https://github.com/anhembedded/Sagittarius-Engine/edit/main/docs/migration/deprecated_apis.md)
