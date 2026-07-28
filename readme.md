# Sagittarius Engine

**A lightweight, modular Python Application Engine for building runtime-driven, extension-based applications.**

Sagittarius Engine is a runtime host — not a web framework, not an ORM, not a DDD framework. It provides the infrastructure layer for building long-running applications: background workers, desktop apps, trading bots, plugin systems, automation pipelines, and CLI tools.

---

## Why Sagittarius Engine?

Most Python frameworks force your application into a specific architecture. Sagittarius Engine takes a different approach: it provides runtime capabilities and gets out of the way.

### What the Engine provides

| Capability | Description |
|---|---|
| **Extension System** | First-class runtime plugins with full lifecycle management (`initialize → start → stop → dispose`). |
| **Dispatcher** | Unified request routing — dispatch commands and queries through registered handlers. |
| **Hosted Services** | Long-running background services managed by the Engine lifecycle. |
| **Scheduler** | Cron-style and interval-based task scheduling with cancellation support. |
| **Task Manager** | Background task pool with cooperative cancellation via `CancellationToken`. |
| **Async Runtime** | Integrated asyncio runtime with thread-safe bridge for sync/async coexistence. |
| **Event Bus** | In-process event publishing and subscription. Sync and async variants available. |
| **EngineContext** | Shared runtime context passed to Extensions and Hosted Services, providing safe access to all Engine capabilities. |
| **Dependency Injection** | Constructor injection with automatic resolution from type hints. |

### What you decide

Your architecture. Your domain. Your database. Your UI framework. Sagittarius Engine provides runtime infrastructure — your application provides the business logic.

---

## Requirements

- Python **3.12** or higher (3.12, 3.13, 3.14)
- Zero mandatory external dependencies (built on the Python Standard Library)

---

## Features

- **Zero mandatory external dependencies** — built on the Python Standard Library core.
- **Extension-based architecture** — extend the Engine at runtime with isolated, reusable plugins (`IExtension` | `IModule`).
- **Full lifecycle management** — deterministic startup and shutdown with ordered extension resolution.
- **Multi-layer Configuration** — `ConfigManager` with chainable `from_json()`, `load_json()`, `load_env()`, and `load_dict()`.
- **Domain Event System** — `IDomainEvent` and `BaseEvent` providing automatic UUID `event_id` and UTC `occurred_on` metadata.
- **Cooperative cancellation** — cancel long-running background tasks gracefully using `CancellationToken`.
- **Unified dispatcher** — route commands and queries through a single `app.dispatch()` call.
- **Multiple Event Bus strategies** — synchronous, thread-pool, and asyncio variants.
- **Remote Audit Dashboard (TUI)** — inspect live engine telemetry (tasks, extensions, health) from a separate terminal via the built-in HTTP telemetry server.
- **SDK templates** — scaffold new Clean Architecture projects with `minimal`, `clean`, `ddd`, or `mvc` templates.

---

## Installation & Integration

### Option 1: Install from GitHub
```bash
pip install git+https://github.com/anhembedded/Sagittarius-Engine.git
```

### Option 2: Local Editable Mode
```bash
pip install -e .
```

### Option 3: Scaffold New Clean Architecture Project
```bash
python -m sagittarius_engine.tools.scaffold my_new_app
```

---

## Quick Start

```python
from sagittarius_engine import App
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from sagittarius_engine.infrastructure.config.config_manager import ConfigManager
from sagittarius_engine.interfaces import IConfig, IContainer, IEventBus

# 1. Initialize core infrastructure
container = StdLibContainer()
event_bus = MemoryEventBus()
app = App(container, event_bus)

# 2. Load configuration seamlessly from file
config = ConfigManager().load_dict({"app.name": "My App"}).load_env()
container.singleton(IConfig, config)
container.singleton(IEventBus, event_bus)

# 3. Boot and stop engine cleanly
app.boot()
print(f"Engine booted: {config.get('app.name')}")
app.stop()
```

---

## Project Templates (SDK)

Use the SDK to scaffold a new project:

```bash
python -m sagittarius_engine.sdk new my_app --template clean
```

Available templates:

| Template | Description |
|---|---|
| `minimal` | Bare-bones App with a single Extension. |
| `clean` | Layered architecture with Domain, Application, Infrastructure, and Adapters. |
| `ddd` | Domain-Driven Design template with Aggregate Roots and Domain Events. |
| `mvc` | Model-View-Controller layout for desktop or CLI apps. |

Generated projects are immediately runnable.

---

## Examples

The `examples/` directory contains reference applications that demonstrate real-world Engine usage.

| Project | Directory | Description |
|---|---|---|
| Student Management | `examples/student_management/` | Full Clean Architecture MVP Desktop (PySide6) & CLI App with SQLite persistence, ConfigManager, and BaseEvent domain events. |
| Desktop Application | `examples/desktop/` | Event-driven PySide6 desktop app with thread-safe UI updates. |
| Worker Service | `examples/worker/` | Background queue consumer with cooperative cancellation. |
| Trading Bot | `examples/trading_bot/` | Long-running strategy loop using `HostedService`, `Scheduler`, and `TaskManager`. |
| WebSocket Client | `examples/websocket/` | Async WebSocket client with reconnect backoff via Async Runtime. |
| Plugin System | `examples/plugin_system/` | Dynamic Extension loading, dependency graph, and activation. |
| REST API | `examples/rest_api/` | Simple HTTP server using the DI Container and Dispatcher. |

---

## Documentation

The full documentation is available at the project docs site (built with MkDocs Material).

| Section | Topics |
|---|---|
| [Getting Started](docs/getting-started/installation.md) | Installation, First App, First Extension, Templates |
| [Concepts](docs/concepts/README.md) | Engine, Runtime, Dispatcher, Event Bus, Middleware, Extensions, Lifecycle |
| [Runtime Guides](docs/runtime/application_lifecycle.md) | Application Lifecycle, Hosted Services, Scheduler, Task Manager, Async Runtime, Cancellation Token |
| [Advanced Guides](docs/advanced/architecture.md) | Extension Dependencies, Architecture, Performance, Best Practices, Troubleshooting |
| [Tutorials](docs/tutorials/README.md) | Desktop App, Worker Service, Trading Bot, WebSocket Client, Plugin System |
| [API Reference](docs/api/index.md) | App, EngineContext, Dispatcher, Event Bus, Scheduler, Task Manager, Hosted Service, Extension, Cancellation Token |
| [Migration Guides](docs/migration/upgrading.md) | Upgrading to v1.0, Deprecated APIs, Migrating from Clean Architecture |

To build and serve the documentation locally:

```bash
pip install -r requirements-docs.txt
mkdocs serve
```

---

## Running Tests

```bash
# Run the full test suite
pytest

# Run documentation code validation only
pytest tests/test_docs.py

# Run with coverage
pytest --cov=sagittarius_engine
```

---

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit your changes following the existing code style.
4. Open a pull request against `develop`.

Please ensure all tests pass and the documentation builds without errors before submitting.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
