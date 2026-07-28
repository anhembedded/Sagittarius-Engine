# TASK-002: `AuditExtension` Framework Observability & Diagnostics Dashboard

- **Status**: ✅ Completed
- **Completion Date**: 2026-07-28
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
    def register(self, ctx: IEngineContext) -> None:
        ctx.container.singleton(AuditService, AuditService(ctx))

    def boot(self, ctx: IEngineContext) -> None:
        if self.enable_dashboard:
            ctx.container.resolve(AuditService).start_server()
```

### 2. `AuditService` Core Inspector
Location: `sagittarius_engine/extensions/audit/audit_service.py`

Gathers telemetry directly from `IEngineContext`:
- `get_loaded_extensions() -> list[str]`
- `get_running_hosted_services() -> list[dict]`
- `get_active_tasks() -> list[dict]` (Iterates `context.tasks.tasks` returning ID, Name, Status, Runtime)
- `get_system_health() -> dict` (Dispatches `HealthCheckQuery`)

### 3. `AuditTerminalDashboard` (Remote Client TUI)
Location: `sagittarius_engine/extensions/audit/terminal_dashboard.py`

Uses a **Client-Server Architecture**. 
- `AuditService` hosts a background HTTP Server (port 9999) serving JSON telemetry.
- The `AuditTerminalDashboard` is a standalone CLI client that uses the `textual` framework to render a beautiful 5-Tab TUI.
- Users open a separate terminal to run the dashboard: `python -m sagittarius_engine.extensions.audit.terminal_dashboard`, avoiding stdout log overlap!
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
