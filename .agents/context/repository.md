# Repository Structure

The `Sagittarius_ForkBoy` repository is organized logically by layer and concern.

## Root Directories

### `sagittarius_engine/`
The core Kernel and Runtime. Contains:
- `kernel/`: Context, App, Dispatcher.
- `runtime/`: TaskManager, Scheduler, AsyncRuntime.
- `interfaces/`: Essential abstractions (`IContainer`, `IEventBus`, `IModule`).
- `extensions/`: Official Kernel extensions (e.g. `audit`, `sqlalchemy`).
- `infrastructure/`: Concrete implementations (`StdLibContainer`, `MemoryEventBus`).
- `sdk/`: Code generation and templating.

### `examples/`
Demonstrates how to build applications using the engine.
- `student_management/`: A complete CQRS/Clean Architecture example.

### `tests/`
Extensive test suite with >80% coverage.
- `kernel/`, `runtime/`, `extensions/`, `infrastructure/`.

### `tools/`
Desktop tools or utilities built ON TOP of the engine.
- `audit_dashboard/`: A PySide6 desktop app that connects to the engine's `AuditExtension` via websockets.

### `Tasks/`
The project's Kanban board. See `.agents/rules/task-tracking.md`.

### `.github/workflows/`
CI/CD pipeline configurations (GitHub Actions).
