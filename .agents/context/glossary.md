# Glossary

* **App / Kernel**: The central entrypoint and orchestrator of the Sagittarius Engine.
* **Extension**: A system-level plugin (e.g. `AuditExtension`) that hooks into the Engine's lifecycle to provide broad capabilities (like logging, telemetry, or ORM binding).
* **Module**: An application-level plugin that registers specific domain logic (Use Cases, Controllers, Repositories) into the DI Container.
* **EventBus**: The messaging infrastructure used to decouple system events (e.g., `TaskStarted`) and domain events (e.g., `StudentAddedEvent`).
* **TaskManager**: The background task runner for asynchronous or threaded jobs.
* **HostedService / BackgroundService**: A long-running daemon process that starts with the `App` and shuts down gracefully with it (e.g. queue listeners, CLI menus).
* **DI Container**: The Dependency Injection container mapping Abstractions (Interfaces) to Concretions.
