---
type: design_doc
tags: [sagittarius, exceptions]
language: python
---

# Exceptions

## Overview
This document covers the custom exceptions defined within the Sagittarius Framework. Using specific exceptions allows for precise error catching and clearer debugging.

## Problem Statement
Relying solely on built-in Python exceptions (like `ValueError` or `Exception`) makes it difficult for developers to programmatically determine *why* a framework operation failed without parsing string messages.

## Proposed Solution
Sagittarius defines a set of specific exceptions extending the base `Exception` class.

## Core API / Interface

### Exceptions (in `src/exceptions.py`)

- `class ModuleRegistrationError(Exception)`: Raised when a module fails to register with the `App` (e.g., trying to use a module that does not implement `IModule`).
- `class DependencyResolutionError(Exception)`: Raised when the `IContainer` fails to resolve a requested dependency (e.g., missing type hints, abstract classes bound to nothing, or circular dependencies).

## Dependencies
- Internal: None
- External: None

## How to Use / Examples

```python
from sagittarius_engine.exceptions import DependencyResolutionError, ModuleRegistrationError
from src.app_kernel import App
from src.interfaces import ILogger

try:
    # Attempting to resolve an unbound interface
    logger = app.container.resolve(ILogger)
except DependencyResolutionError as e:
    print(f"Setup incomplete: {e}")

try:
    # Attempting to register an invalid object as a module
    app.use(object())
except ModuleRegistrationError as e:
    print(f"Invalid module provided: {e}")
```

## Implementation Notes
- Currently, these exceptions are simple subclasses of `Exception` with no custom properties, relying on standard message passing `raise ExceptionClass("Message")`.

## Related Documents
- `container.md`
- `app_kernel.md`
