# Configuration

Configuration in Sagittarius Engine is typically loaded into an `IConfig` abstraction.

## Patterns
- **Pydantic**: Use `pydantic.BaseSettings` for robust, typed configuration that can read from Environment Variables, `.env` files, or JSON.
- **Dependency Injection**: Configuration settings should be registered in the Container during the Module's `register()` phase.

## Extensibility
- Extensions like `AuditExtension` can accept configuration parameters on initialization (e.g., `AuditExtension(port=8765)`).
- Tools (like `audit_dashboard`) manage their own configs independent of the Engine Kernel.
