# Anti-Pattern Case Studies (Binance Bot)

This document tracks architectural mistakes (anti-patterns) made during development, the reasoning behind the correction, and how to prevent them in the future.

## 1. The God Object `main.py`
**Mistake**: Putting CLI parsing, DI container configuration, AsyncIO loop management, and Application Bootstrapping all inside `main.py`.
**Correction**: 
- Moved DI configuration to `binance_bot_module.py` (BaseModule).
- Moved CLI parsing to `presentation/cli/cli_parser.py`.
- `main.py` is now strictly a Composition Root that coordinates the Parser and the App Boot sequence.

## 2. Python Class as Config
**Mistake**: Creating `app_config.py` and `user_config.py` with Dataclasses holding hardcoded "Magic Numbers".
**Correction**: 
- Used Sagittarius Engine's built-in `IConfig` and `ConfigManager`.
- Migrated configs to `app_config.json` and `user_config.json`.
- Registered `IConfig` in the DI container for loose coupling.

## 3. Blocking the Main Thread for Background Tasks
**Mistake**: Running `asyncio.run()` in an infinite `while True` loop inside `stream_cmd.py` to keep a WebSocket connection alive.
**Correction**: 
- Inherited `IHostedService` for `BinanceWebsocketService`.
- Used `context.async_runtime.run_coroutine(...)` to schedule the background loop on the engine's dedicated async thread.
- Let the Engine manage the lifecycle (`start`/`stop`) of the service automatically during `app.boot()`.

## 4. Misusing `IExtension` for Application Logic
**Mistake**: Creating `DataSyncExtension` and `LiveStreamExtension` under `src/application/extensions` to register Use Cases and Repositories.
**Correction**: 
- `IExtension` is meant for Framework Infrastructure (Logger, Metrics, Health).
- Business Domain Logic must be encapsulated in an `IModule` (inheriting from `BaseModule`).
- Created `BinanceBotModule` at the root of `src/` to properly register all Domain dependencies, aligning with the Bounded Context principles.

## 5. Unnecessary Lambda Wrappers for Singletons
**Mistake**: Using `container.singleton(IEventBus, lambda c: event_bus)` to register an existing instance.
**Correction**: 
- `StdLibContainer.singleton()` accepts existing instances directly.
- The correction simply passes the instance: `container.singleton(IEventBus, event_bus)`. This keeps the composition root clean and prevents redundant factory invocations.

## 6. Leaking Low-Level OS Code in Composition Root
**Mistake**: Using raw `os.path.join(os.path.dirname(__file__), ...)` directly in `main.py` to construct config paths, making the code verbose and unreadable.
**Correction**:
- Extracted path resolution logic into a framework-level utility `PathUtils.get_relative_path(...)` inside `sagittarius_engine.utils`.
- Updated `.agents/rules/code-rule.md` to forbid raw low-level operations in the application layer.

## 7. Ignoring Built-in Framework Extensions (Logging)
**Mistake**: Manually setting up `logging.basicConfig()` inside `main.py` when Sagittarius Engine already provides a `LoggerExtension`.
**Correction**:
- Removed manual `setup_logging()`.
- Used `app.use(LoggerExtension())` to let the framework standardize logging configuration.
