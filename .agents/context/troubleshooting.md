# Troubleshooting Guide

Solutions to common issues.

## 1. Async Context Errors (`RuntimeError: Event loop is closed`)
- **Cause**: Trying to spawn a task after the `AsyncRuntime` has been stopped.
- **Fix**: Ensure background tasks check the `CancellationToken` (e.g. `token.is_cancelled`) and exit gracefully before the app fully shuts down.

## 2. Mypy Type Errors (`Liskov substitution principle violation`)
- **Cause**: A child class overrides a method with a different signature than the interface.
- **Fix**: Ensure module `register(self, app: App)` matches `IModule.register(self, app: App)` exactly.

## 3. Tool Dashboard (PySide6) Not Receiving Data
- **Cause**: The engine's `AuditExtension` websocket might not be running or bound to the correct port.
- **Fix**: Check that `app.use(AuditExtension(port=8765))` is called in the engine. Ensure the Tool is connecting to `ws://localhost:8765`.

## 4. Circular Imports
- **Cause**: Domain models importing infrastructure details.
- **Fix**: Use `from typing import TYPE_CHECKING` and `if TYPE_CHECKING:` to resolve typing circular dependencies. Enforce Dependency Inversion.
