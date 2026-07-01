---
type: design_doc
tags: [sagittarius, middleware]
language: python
---

# Middleware

## Overview
Middleware in Sagittarius acts as filters that wrap around the execution of Commands and Queries. Following the Onion architecture or Interceptor pattern, they intercept requests before they reach the core handler, and intercept results/exceptions on the way out.

## Problem Statement
Cross-cutting concerns like logging, input validation, transaction management, and performance timing shouldn't be hardcoded into every Command or Query handler. Doing so violates the Single Responsibility Principle and creates code duplication. Middleware extracts these concerns into reusable components.

## Proposed Solution
The `IMiddleware` interface defines a `process()` method. The `MiddlewarePipeline` (part of the App Kernel) recursively chains these middlewares. Calling `next_handler()` inside the `process()` method yields control to the next middleware in the chain, eventually reaching the core logic.

The framework provides several built-in middlewares:
- **`LoggingMiddleware`**: Logs before and after command execution, using an injected `ILogger`.
- **`TimingMiddleware`**: Calculates and prints the exact milliseconds it took to execute the command.
- **`ValidationMiddleware`**: Basic sanity checks on DTOs.
- **`PydanticValidationMiddleware`**: Validates raw dicts or objects against a strict `pydantic.BaseModel` schema.

## Core API / Interface

### `interface IMiddleware` (in `src/interfaces/i_middleware.py`)
- `def process(self, cmd_or_query: Any, data_transfer_obj: Any, next_handler: Callable[[], Any]) -> Any`: Processes the request and calls `next_handler()` to continue the pipeline.

### Implementations

#### `class LoggingMiddleware(IMiddleware)`
- `def __init__(self, container: IContainer)`: Needs container to resolve the `ILogger`.

#### `class TimingMiddleware(IMiddleware)`
- `def process(...)`: Times execution using `time.time()`.

#### `class ValidationMiddleware(IMiddleware)`
- Basic None check validation.

#### `class PydanticValidationMiddleware(IMiddleware)`
- `def __init__(self, model_class: Any) -> None`: Takes a Pydantic `BaseModel` class.
- Will convert `dict` or object `__dict__` into a validated Pydantic model. Raises `ValueError` on validation failure.

## Dependencies
- Internal: `IContainer`, `ILogger`
- External: `time` (stdlib), `pydantic` (optional, strictly fallback to `ImportError` if not installed)

## How to Use / Examples

```python
from src.interfaces import IContainer
from src.middleware.logging_middleware import LoggingMiddleware
from src.middleware.timing_middleware import TimingMiddleware

def setup_middleware(app: 'App', container: IContainer):
    # Middlewares execute in the order they are added.
    # Here, TimingMiddleware wraps LoggingMiddleware, which wraps the command.
    app.use_middleware(TimingMiddleware())
    app.use_middleware(LoggingMiddleware(container))

class CustomAuthMiddleware(IMiddleware):
    def process(self, cmd_or_query, data_transfer_obj, next_handler):
        print("Checking permissions...")
        if data_transfer_obj.get("user_id") != 1:
            raise PermissionError("Access Denied")

        # Proceed down the pipeline
        result = next_handler()

        print("Command finished, cleaning up...")
        return result
```

## Implementation Notes
- **Order Matters**: Middlewares run in the exact order they are added to the pipeline. The first middleware added is the outermost layer.
- **Exceptions**: If a middleware (or the core command) raises an exception *after* calling `next_handler()`, that exception propagates back up through the previously executed middlewares.
- **Pydantic**: The `PydanticValidationMiddleware` uses a `try/except ImportError` strategy. It will raise a standard python `ImportError` at instantiation time if `pydantic` is not pip-installed.

## Related Documents
- `app_kernel.md` (where `MiddlewarePipeline` lives)
