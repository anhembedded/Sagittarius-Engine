> Applies to Sagittarius Engine v1.x

# Upgrading to v1.0

## Overview

This guide provides a step-by-step checklist for upgrading your application from Sagittarius Engine `v0.x` to `v1.x`. 

The `v1.x` release focuses heavily on modularity. Most of the required changes involve updating your import statements to point to the new Extension packages instead of the monolithic core.

## Upgrade Checklist

### Step 1: Update the Dependency

Update your `requirements.txt` or `pyproject.toml` to target the `v1.x` release of Sagittarius Engine.

```toml
# pyproject.toml
[project]
dependencies = [
    "sagittarius-engine>=1.0.0,<2.0.0"
]
```

### Step 2: Surface Deprecation Warnings

Before changing any code, run your application's test suite with Python's warning filter set to `default`. This will print out exactly which deprecated APIs your application is currently using.

```bash
# Run pytest and show all warnings
python -W default -m pytest
```

Take note of any `DeprecationWarning`s originating from `sagittarius_engine`.

### Step 3: Update Imports

Change all imports pointing to the old core locations to their new Extension locations.

#### CQRS Updates
```diff
- from sagittarius_engine.interfaces import ICommand, IQuery
+ from sagittarius_engine.extensions.cqrs import ICommand, IQuery
```

#### Persistence Updates
```diff
- from sagittarius_engine.base import BaseRepository
+ from sagittarius_engine.extensions.persistence import BaseRepository

- from sagittarius_engine.infrastructure.persistence import ISession, DatabaseModule
+ from sagittarius_engine.extensions.persistence import ISession, DatabaseExtension
```

### Step 4: Migrate "Modules" to "Extensions"

Search your codebase for any classes implementing `IModule` or ending in `Module`. Rename them to `Extension`.

```diff
from sagittarius_engine import App
- from sagittarius_engine.extensions.logger_module import LoggerModule

app = App(container, event_bus)
- app.use(LoggerModule())
+ from sagittarius_engine.extensions.logger_module import LoggerExtension
+ app.use(LoggerExtension())
```

### Step 5: Replace `execute` and `query`

Search your application for any calls to `app.execute()` and `app.query()`.

```diff
- result = app.execute(CreateUserCommand, dto)
+ result = app.dispatch(CreateUserCommand, dto)

- user = app.query(GetUserQuery, user_id)
+ user = app.dispatch(GetUserQuery, user_id)
```

> [!NOTE]
> The `execute()` method on your actual command handlers (e.g., `def execute(self, dto):`) remains unchanged. You only need to update the method called on the `Dispatcher` or `App` facade.

### Step 6: Verify Tests

Run your test suite again.

```bash
python -W error -m pytest
```

By using `-W error`, Python will treat any remaining `DeprecationWarning`s as hard errors, ensuring that your codebase is fully compliant with `v1.0`.

## Need Help?

If you encounter unexpected errors during migration, consult the [Troubleshooting](../advanced/troubleshooting.md) guide or read the detailed explanation of the [Architectural Shifts](from_clean_architecture.md).

> [Found an issue? Edit this page on GitHub.](https://github.com/anhembedded/Sagittarius-Engine/edit/main/docs/migration/upgrading.md)
