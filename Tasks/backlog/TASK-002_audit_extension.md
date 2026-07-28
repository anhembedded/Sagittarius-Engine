# TASK-002: `AuditExtension` Framework Observability & Diagnostics Dashboard

- **Status**: 📝 Planned (Backlog)
- **Priority**: P1 - High
- **Category**: Observability / Diagnostics

---

## 🎯 Goal
Provide a built-in Framework Observability & Diagnostics Extension (`AuditExtension`) that inspects live engine runtime telemetry via `IEngineContext` and renders a real-time interactive terminal dashboard (CLI Inspector) or JSON telemetry audit log.

---

## 🏛️ Background & Motivation
As applications grow (Trading Bots, IoT systems, Desktop Apps), developers need clear visibility into:
1. Which Extensions / Modules are loaded in the Engine.
2. Which `IHostedService` instances are currently RUNNING.
3. Which Background Tasks (`ITaskHandle`) are active, pending, or completed.
4. Total thread count, uptime, and system health status (`HealthCheckQuery`).

---

## 📐 Architecture & Design

### 1. `AuditExtension` Class
Location: `sagittarius_engine/extensions/audit/audit_extension.py`

```python
from sagittarius_engine.interfaces import IEngineContext, IExtension


class AuditExtension(IExtension):
    def initialize(self, ctx: IEngineContext) -> None:
        ctx.container.singleton(AuditService, AuditService(ctx))

    def start(self, ctx: IEngineContext) -> None:
        pass
```

### 2. `AuditService` Core Inspector
Location: `sagittarius_engine/extensions/audit/audit_service.py`

Gathers telemetry directly from `IEngineContext`:
- `get_loaded_extensions() -> list[str]`
- `get_running_hosted_services() -> list[dict]`
- `get_active_tasks() -> list[dict]` (Iterates `context.tasks.tasks` returning ID, Name, Status, Runtime)
- `get_system_health() -> dict` (Dispatches `HealthCheckQuery`)

### 3. `AuditTerminalDashboard` (CLI Inspector)
Location: `sagittarius_engine/extensions/audit/terminal_dashboard.py`

Provides a clean ANSI-formatted Terminal UI:
```text
================================================================================
                    SAGITTARIUS ENGINE - AUDIT DASHBOARD
================================================================================
 🟢 Health: OK | ⏱️ Uptime: 00:08:15 | 🧵 Active Tasks: 3
--------------------------------------------------------------------------------
 📦 EXTENSIONS: LoggerExtension, DatabaseExtension, HealthModule, AuditExtension
 ⚙️ HOSTED SERVICES: TerminalMenu (RUNNING), MetricsPublisher (RUNNING)
 🧵 TASKS:
    - [c4f81a9c] TerminalUI           (RUNNING)   [00:08:15]
    - [a1b2c3d4] AsyncGPAPipeline     (COMPLETED) [00:00:02]
================================================================================
```

---

## 📋 Implementation Checklist
- [ ] Create `sagittarius_engine/extensions/audit/` package.
- [ ] Implement `AuditService` querying `IEngineContext`.
- [ ] Implement `AuditExtension` implementing `IExtension`.
- [ ] Implement `AuditTerminalDashboard` CLI inspector.
- [ ] Write unit tests in `tests/test_audit_extension.py`.
