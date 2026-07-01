---
type: design_doc
tags: [sagittarius, module, database]
language: python
---

# DatabaseModule

## Overview
The `DatabaseModule` is a built-in module that handles the instantiation of database engines and sessions, registering them into the framework's Dependency Injection container.

## Problem Statement
Establishing database connections, managing connection pooling, and creating thread-local sessions (Unit of Work) requires significant boilerplate. Hardcoding this setup directly inside `main.py` pollutes the composition root and makes testing difficult.

## Proposed Solution
Sagittarius provides the `DatabaseModule` which automatically reads the `database.url` from `IConfig`. It attempts to initialize a SQLAlchemy Engine and registers a thread-safe `scoped_session` wrapped in an `ISession` adapter into the `IContainer`.

## Core API / Interface

### `class SQLAlchemySessionAdapter(ISession)` (in `src/modules/database_module.py`)
Wraps a SQLAlchemy session to conform to the `ISession` interface.
- `def commit(self) -> None`
- `def rollback(self) -> None`
- `def execute(self, statement: Any, params: Any = None) -> Any`
- `def query(self, *entities: Any) -> Any`

### `class DatabaseModule(BaseModule)` (in `src/modules/database_module.py`)
- `def register(self, app: App) -> None`: Reads config, sets up SQLAlchemy `create_engine` and `scoped_session`, and registers the `ISession` singleton.

## Dependencies
- Internal: `BaseModule`, `App`, `IConfig`, `ISession`, `ILogger`
- External: `sqlalchemy` (Optional. Fails gracefully with a warning if not installed).

## How to Use / Examples

```python
from src.app_kernel import App
from src.modules.database_module import DatabaseModule

# Assuming container and config are setup with database.url = 'sqlite:///app.db'
app.use(DatabaseModule())

# Elsewhere in a Command or Repository, ISession is automatically injected:
# class UserRepository:
#     def __init__(self, session: ISession):
#         self.session = session
```

## Implementation Notes
- **Graceful Degradation**: If `sqlalchemy` is not installed, the module logs a warning and exits without crashing the app.
- **Default Database**: If `IConfig` cannot be resolved or does not contain `database.url`, it falls back to an in-memory SQLite database (`sqlite:///:memory:`).

## Related Documents
- `base_repository.md`
- `configuration.md`
