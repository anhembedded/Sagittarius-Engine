---
type: design_doc
tags: [sagittarius, logging]
language: python
---

# Logging

## Overview
The Logging component provides a unified mechanism for recording application state, errors, and informational messages. It encapsulates Python's standard `logging` library behind an interface, allowing developers to swap out the logging implementation if needed (e.g., to a structured JSON logger) without altering the application code.

## Problem Statement
Directly utilizing `print()` or Python's built-in `logging.getLogger()` throughout a codebase binds the application to specific formatting and output sinks, creating side-effects that are difficult to manage and test. A central interface allows consistent configuration (like log levels and log files) dynamically driven by the environment.

## Proposed Solution
Sagittarius defines the `ILogger` interface. The `StdLogger` implementation wraps Python's standard `logging` module and automatically reads settings (`log.level`, `log.file`) from an injected `IConfig` instance.
The `LoggerModule` is a provided module that automatically registers `StdLogger` into the framework's DI Container during the application boot phase.

## Core API / Interface

### `interface ILogger` (in `src/interfaces/i_logger.py`)
- `def info(self, message: str) -> None`: Logs an informational message.
- `def warning(self, message: str) -> None`: Logs a warning message.
- `def error(self, message: str) -> None`: Logs an error message.
- `def debug(self, message: str) -> None`: Logs a debug message.

### `class StdLogger(ILogger)` (in `src/infra/std_logger.py`)
Implementation using `logging`.
- `def __init__(self, config: Optional[IConfig] = None)`: Reads config for `log.level` (e.g., 'DEBUG') and `log.file` (e.g., 'app.log'). If a file is specified, it attaches a `FileHandler` in addition to the `StreamHandler`.

### `class LoggerModule(BaseModule)` (in `src/modules/logger_module.py`)
A module to automatically wire the Logger into the Container.
- `def register(self, app: App) -> None`: Attempts to resolve `IConfig`. It instantiates `StdLogger` and registers it as a Singleton bound to `ILogger`.
- `def boot(self, app: App) -> None`: No-op.

## Dependencies
- Internal: `IConfig`, `BaseModule`, `App`
- External: Standard libraries (`logging`, `sys`)

## How to Use / Examples

```python
from src.app_kernel import App
from sagittarius_engine.infrastructure.std_container import StdLibContainer
from sagittarius_engine.infrastructure.memory_event_bus import MemoryEventBus
from sagittarius_engine.infrastructure.dict_config import DictConfig
from src.interfaces import IConfig, ILogger
from sagittarius_engine.extensions.logger_module import LoggerModule

container = StdLibContainer()
event_bus = MemoryEventBus()

# Setup config
config = DictConfig()
config.set("log.level", "DEBUG")
config.set("log.file", "sagittarius.log")
container.singleton(IConfig, config)

app = App(container, event_bus)

# Register the Logger Module
app.use(LoggerModule())

# Resolve and use the logger
logger = container.resolve(ILogger)
logger.info("Application is starting...")
```

## Implementation Notes
- **Handler Cleanup**: To prevent `ResourceWarning` (unclosed file exceptions) often seen during Pytest execution, `StdLogger` explicitly iterates over existing active handlers in the standard library logger (`logging.getLogger("App")`), executes `handler.close()`, and removes them before attaching new ones.
- **Auto-Resolution**: The `App` instance inherently looks for an `ILogger` bound in the container (via the private `_get_logger()` method) to log its own boot sequence and query executions gracefully.

## Related Documents
- `configuration.md`
- `modules.md`
