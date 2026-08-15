> Applies to Sagittarius Engine v1.x

# Migrating from Clean Architecture

## Overview

In `v1.x`, Sagittarius Engine officially moves away from a rigid "Clean Architecture" pattern (often described as `Business Layer`, `UseCase Layer`, and `Repository Layer`) in favor of a flexible **Extension-based Architecture**. 

This document explains why the shift happened and how to adapt your application's design to the modern approach.

## Why the Shift?

While Clean Architecture is excellent for isolating domain logic, hardcoding infrastructure abstractions like `Repository Layer` directly into the engine's core made the framework inflexible. 

In `v0.x`, every application was forced to use the `BaseRepository` class, even if it didn't use a database (e.g., a stateless proxy server). 

By migrating to an **Extension-based Architecture**, the engine core now focuses exclusively on the runtime lifecycle, event distribution, and background execution. Features like CQRS and Persistence are now decoupled plugins (Extensions) that you opt into.

## Key Paradigm Shifts

### 1. From "Application Framework" to "Engine"
- **Old Concept:** You build a "Clean Architecture Application".
- **New Concept:** You build your application on top of the "Sagittarius Engine", using Extensions to wire up your specific architecture.

### 2. The Disappearance of "Layers" in the Engine
The engine no longer enforces where you place your business logic. 
- You are free to structure your application using Clean Architecture, Hexagonal Architecture, or a simple MVC pattern. 
- The engine's job is simply to execute it via the `Dispatcher`.

### 3. "Modules" are now "Extensions"
- **Old Terminology:** `Module` (e.g., `DatabaseModule`)
- **New Terminology:** `Extension` (e.g., `DatabaseExtension`)

The term "Module" conflicted with Python's built-in file modules, causing communication friction. All plugins that hook into the Engine's lifecycle are now formally called **Extensions**.

## Migrating Your Codebase

### Step 1: Remove Rigid Base Classes

If your code previously relied on `sagittarius_engine.base.BaseRepository`, you must now use the explicit `sagittarius_engine.extensions.persistence` extension.

```python
# Old (v0.x)
# non-runnable
from sagittarius_engine.base import BaseRepository


class UserRepository(BaseRepository): ...
```

```python
# New (v1.x)
# non-runnable
from sagittarius_engine.extensions.persistence import BaseRepository


class UserRepository(BaseRepository): ...
```

### Step 2: Extract Business Logic into Handlers

Rather than executing monolithic UseCases directly, you should encapsulate domain logic into decoupled handlers and route them through the `Dispatcher`.

```python
# Old (v0.x)
# non-runnable
use_case = CreateUserUseCase(repo)
user = use_case.execute(dto)
```

```python
# New (v1.x)
# non-runnable
from sagittarius_engine import App
from sagittarius_engine.extensions.cqrs import ICommand


class CreateUserCommand(ICommand):
    def execute(self, dto: dict) -> str:
        # Domain logic here
        return "Success"


# The Dispatcher routes the command to the correct handler automatically
result = app.dispatch(CreateUserCommand, dto)
```

## Summary

You do not need to rewrite your business logic. You only need to change how that logic is wired into the framework. By treating CQRS and Persistence as optional Extensions rather than mandatory layers, your application becomes significantly more modular.

## Next Steps

- Review the [Deprecated APIs](deprecated_apis.md) guide.
- Follow the [Upgrading to v1.0](upgrading.md) step-by-step tutorial.

> [Found an issue? Edit this page on GitHub.](https://github.com/anhembedded/Sagittarius-Engine/edit/main/docs/migration/from_clean_architecture.md)
