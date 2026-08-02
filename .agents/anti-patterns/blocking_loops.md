# Anti-Pattern: Blocking Event Loops in Custom CLI Services

## The Mistake
Creating custom "infinite loop" CLI commands (like manually running `asyncio.run(run_stream())` and blocking the main thread using `while True`) for long-running processes, instead of utilizing the Framework's built-in `IHostedService` or `BackgroundService` runtime abstractions.

## Why it is an Anti-Pattern
1. **Bypasses Framework Lifecycle:** By blocking the main thread, we circumvent `app.boot()` and `app.stop()` graceful lifecycle management for other background services.
2. **Reinvents the Wheel:** Sagittarius Engine already has `HostedServiceManager` and `AsyncRuntime` specifically designed to run daemon processes asynchronously in the background while the application runs.
3. **Violates Clean Architecture:** Forces the Presentation layer (`main.py` or CLI handlers) to handle low-level asynchronous runtime execution logic.

## The Solution
1. Inherit from `IHostedService` (or `BackgroundService`).
2. Run async tasks using `context.async_runtime.run_coroutine(...)` within the `start()` method.
3. Register the service in the extension via `context.hosted_services.register(MyBackgroundService)`.
4. The CLI simply boots the app, lets it run, and catches `KeyboardInterrupt` to call `app.stop()`.
