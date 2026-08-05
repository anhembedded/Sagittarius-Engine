# Module: Logging

## 1. Overview
The Logging module in `sagittarius_engine` provides a centralized, flexible, and structured logging system. It abstracts away the default Python `logging` module behind an `ILogger` interface, ensuring that the core application domain and use cases are decoupled from external logging frameworks. It inherently supports structured metadata (via `extra` fields), and integrates seamlessly with the framework's Dependency Injection container and external log viewers.

## 2. Terminology
- **ILogger**: The core pure Python interface defining logging operations (`info`, `debug`, `warning`, `error`).
- **StdLogger**: The primary concrete implementation of `ILogger` that wraps Python's built-in `logging` library and configures handlers (Console, File, TCP).
- **LoggerConfig**: A configuration utility class that maps settings from `IConfig` to initialize the `StdLogger`.
- **TcpLogViewerHandler**: A custom Python `logging.Handler` that serializes log records as JSON and streams them to a centralized Log Viewer application over TCP.

## 3. Use Cases
- **Standard Application Logging**: Recording the internal state, tracing execution paths, and identifying errors during development and production.
- **Remote Log Monitoring**: Using `TcpLogViewerHandler` to monitor real-time execution of the engine across multiple services on a centralized UI (Log Viewer).
- **Domain & Application Layer Logging**: Logging business events in a completely decoupled way by injecting `ILogger` without depending on Python's built-in `logging` module.

## 4. How it works
During the application boot process, the `LoggerExtension` (`sagittarius_engine.extensions.logger.logger_module`) resolves the active configuration (`IConfig`) and instantiates a `StdLogger`.
1. `StdLogger` creates a root-level Python logger named `"App"`.
2. It reads `LoggerConfig` to determine which Handlers to attach (e.g., `StreamHandler` for Console, `FileHandler`, and `TcpLogViewerHandler`).
3. The `StdLogger` instance is then registered into the DI Container as a Singleton bound to `ILogger`.
4. Any log called via `ILogger.info()` passes through `StdLogger`, adds the `extra` structured data, and delegates to the root `"App"` logger.
5. Child loggers initialized via `logging.getLogger("App.XYZ")` implicitly inherit this configuration because Python propagates their logs up to `"App"`.

## 5. Components & API

### Core Interfaces
- **`sagittarius_engine.interfaces.i_logger.ILogger`**
  ```python
  def info(self, message: str, extra: dict[str, Any] | None = None) -> None: ...
  def debug(self, message: str, extra: dict[str, Any] | None = None) -> None: ...
  def warning(self, message: str, extra: dict[str, Any] | None = None) -> None: ...
  def error(self, message: str, extra: dict[str, Any] | None = None) -> None: ...
  ```

### Concrete Implementations
- **`StdLogger`** (`sagittarius_engine.infrastructure.logging.std_logger.StdLogger`): The production default. Manages attaching handlers (File, Console, TCP) based on the application configuration.

## 6. Code Examples & Usage Guide

### Recommended Clean Architecture Usage (Injecting `ILogger`)
The absolute best practice inside your Application or Domain layers is to rely entirely on dependency injection:

```python
from sagittarius_engine.interfaces import ILogger
from Binace_Bot.src.application.ports.i_market_data_repository import IMarketDataRepository

class SyncMarketDataCommandHandler:
    def __init__(self, repository: IMarketDataRepository, logger: ILogger) -> None:
        self.repository = repository
        self.logger = logger

    def execute(self, command) -> None:
        self.logger.info("Starting sync process", extra={"symbol": command.symbol})
```

### Framework/Convenience Usage (Python's Built-in Logger)
Because `StdLogger` configures the global logger named `"App"`, you can securely use Python's built-in mechanism to create namespaced loggers. This avoids DI overhead but slightly couples your code to the Python `logging` module.

```python
import logging

class GetHistoricalKlinesQueryHandler:
    def __init__(self, repository: IMarketDataRepository) -> None:
        self.repository = repository
        # Creates a child logger. Logs automatically propagate up to "App"
        # and are processed by StdLogger's handlers (Console, File, TCP Viewer).
        self.logger = logging.getLogger("App.QueryHandler")

    def execute(self, query) -> list:
        self.logger.debug(f"Fetching klines for {query.symbol}")
        # ...
```

## 7. Common Misconceptions

1. **Misconception: `logging.getLogger("App.XYZ")` bypasses the framework's configuration.**
   - **Truth**: As long as the prefix is `"App."`, the standard propagation mechanics in Python will route the log directly to the root `"App"` logger managed by `StdLogger`. It still benefits from the TCP Log Viewer and File logging configurations without needing an injected instance.

2. **Misconception: You must use `logging.getLogger(__name__)` everywhere.**
   - **Truth**: If you use `__name__` (e.g., `Binace_Bot.src.application...`), your logs will NOT propagate to `"App"` unless you manually rewire the loggers. Always prefix your namespace with `"App."` (e.g., `"App.Database"`) to hook into `StdLogger`.

3. **Misconception: `extra` dictionaries are printed directly in the console output.**
   - **Truth**: By default, Python's `StreamHandler` string formatter `%(message)s` does NOT print the `extra` dict. The structured `extra` data is primarily utilized by the `TcpLogViewerHandler` which serializes it to JSON, allowing rich UI sorting and filtering on the viewer app.

4. **Misconception: Injecting `ILogger` is overkill and redundant.**
   - **Truth**: Injecting `ILogger` is strictly required in the inner layers (Domain) if you want to maintain 100% adherence to Clean Architecture. It makes testing easier (you can inject a Mock logger) and prevents your domain core from tightly coupling to Python's `logging` module implementations.
