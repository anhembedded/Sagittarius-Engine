# Audit Extension (Telemetry & Diagnostics)

The `Audit` module in Sagittarius Engine is a core extension responsible for system observability, diagnostics, and real-time telemetry. It acts as the "nervous system" monitor of the Engine, tracking active tasks, memory consumption, loaded extensions, and event history.

---

## 1. Overview

The Audit Extension provides deep introspective capabilities for the Kernel. Its primary responsibility in the Clean Architecture is to act as an infrastructural cross-cutting concern. It does not dictate business logic but strictly observes the runtime state.

When enabled, it launches a background telemetry server that broadcasts the entire internal state of the `EngineContext` (Scheduler, TaskManager, Middleware Pipeline, DI Container) to any connected clients (such as the `audit_dashboard` PySide6 application).

---

## 2. How it works

The Audit module operates through a reactive, event-driven mechanism combined with background daemon threads:

1. **Lifecycle Integration**: During the `App.boot()` phase, the `AuditExtension` is initialized. If configured with `enable_dashboard=True`, it spawns the telemetry server.
2. **Reactive Telemetry (No Polling)**: Instead of constantly polling the system in a tight loop (which wastes CPU), the `AuditService` registers listeners on the `EventBus`. It waits for significant lifecycle events (e.g., `TaskStarted`, `TaskCompleted`, `TaskFailed`, or domain events like `student.added`).
3. **State Snapshotting**: When an event fires, `AuditService` takes a full snapshot of the Engine (calculating Uptime, Memory via `psutil`, listing all running Tasks and Hosted Services).
4. **Daemon Threading**: The `WebsocketBroadcaster` runs in a dedicated daemon thread. It uses an internal `asyncio` event loop to manage multiple concurrent WebSocket clients, ensuring that broadcasting telemetry never blocks the main Engine thread.

---

## 3. Components & API

### Core Interfaces & Classes

* **`AuditExtension`**: The `IExtension` implementation. It registers dependencies and manages the boot/shutdown lifecycle of the telemetry server.
* **`AuditService`**: The aggregator. It accesses the `IEngineContext` to read raw system data and format it into a comprehensive dictionary (JSON).
* **`ITelemetryBroadcaster`**: The abstract port (interface) defining how telemetry should be sent (`start()`, `stop()`, `broadcast(event, payload)`).
* **`WebsocketBroadcaster`**: The concrete implementation of `ITelemetryBroadcaster`. It opens a WebSocket server (default port `9999`) and pushes stringified JSON to all connected clients.

---

## 4. Usage Guide

### Initializing the Audit Extension

To enable telemetry in your Sagittarius application, you simply register the extension before booting the app:

```python
from sagittarius_engine.kernel.app import App
from sagittarius_engine.extensions.audit.audit_extension import AuditExtension

app = App()

# Register the Audit Extension and turn on the WebSocket telemetry server
app.use(AuditExtension(enable_dashboard=True))

# Start the application
app.boot()
```

### Accessing Audit Data Programmatically

If you are inside a Use Case or another Module and need to access the system metrics directly (without websockets), you can resolve the `AuditService` from the DI Container:

```python
from sagittarius_engine.extensions.audit.audit_service import AuditService


def my_diagnostic_command(context: IEngineContext):
    # Resolve the service
    audit = context.container.resolve(AuditService)

    # Get direct metrics
    uptime = audit.get_uptime_seconds()
    tasks = audit.get_active_tasks()

    print(
        f"Engine has been running for {uptime} seconds with {len(tasks)} active tasks."
    )
```

---

## 5. Common Misconceptions

### ❌ Misconception 1: The Audit service severely degrades engine performance by constantly calculating CPU and Memory usage

✅ **Truth**: The `AuditService` is strictly **reactive**. It only calculates system resources and pushes state snapshots when a registered Event actually fires on the `EventBus` (e.g., a Task starts or finishes). It does not run a continuous blocking `while True` loop to poll data, ensuring negligible performance overhead.

### ❌ Misconception 2: Connecting multiple clients to the telemetry server will block the main application thread

✅ **Truth**: The `WebsocketBroadcaster` runs entirely on an isolated background daemon thread using its own asynchronous event loop. Network I/O and client management are completely decoupled from the main Engine execution context.

### ❌ Misconception 3: You must use the official PySide6 `audit_dashboard` to view the engine's telemetry

✅ **Truth**: The engine simply broadcasts standard JSON over an open WebSocket connection (default: `ws://localhost:9999`). Any standard WebSocket client—whether it's a React frontend web app, a Vue dashboard, a simple Python script, or Postman—can connect and consume the real-time `state_update` payloads.
