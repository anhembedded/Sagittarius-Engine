# Sagittarius Engine Roadmap v1

## 🎯 Vision

Từ:
```text
Sagittarius = Clean Architecture Framework
```
↓
Đến:
```text
Sagittarius = Lightweight Modular Application Engine
```

Kernel provides capabilities.
Applications choose architecture.
Extensions integrate technologies.
SDK accelerates development.

```text
                 Sagittarius

            ┌──────────────────┐
            │      Kernel      │
            └──────────────────┘
                     ▲
                     │
            ┌──────────────────┐
            │  Runtime Infras. │   ← Phase 7
            └──────────────────┘
                     ▲
                     │
            ┌──────────────────┐
            │       SDK        │
            └──────────────────┘
                     ▲
                     │
            ┌──────────────────┐
            │   Applications   │
            └──────────────────┘
                     ▲
                     │
            ┌──────────────────┐
            │    Ecosystem     │
            └──────────────────┘
```

---

# Foundation Migration (Completed)

Đây là phần đã hoàn thành.

---

## ✅ Phase 1 — Architecture Renaming

**Status:** Completed

### Goal
Loại bỏ tư duy "Application Framework".

### Completed
* application → kernel
* ports → interfaces
* modules → extensions
* infrastructure restructuring
* package cleanup

---

## ✅ Phase 2 — Kernel Decomposition

**Status:** Completed

### Goal
Biến App thành façade.

### Completed
```text
kernel/
    app.py
    bootstrap.py
    dispatcher.py
    lifecycle.py
    module_loader.py
```

---

## ✅ Phase 2.5 — EngineContext

**Status:** Completed

### Goal
Central Runtime Context.

### Completed
```text
EngineContext
    container
    dispatcher
    event_bus
    logger
    config
    middleware
    extensions
```

---

## ✅ Phase 3 — Engine Decoupling

**Status:** Completed

### Goal
Kernel không còn biết Clean Architecture.

### Completed
* CQRS → Extension
* Repository → Extension
* SQLAlchemy → Extension
* Database → Extension
* Compatibility Shims

---

## ✅ Phase 4 — Extension Runtime

**Status:** Completed

### Goal
Extension trở thành first-class runtime object.

### Completed
* IExtension
* ExtensionDescriptor
* Dependency Graph
* Topological Sort
* Rollback
* Lifecycle Events
* Startup Ordering
* Shutdown Ordering
* Compatibility Layer

---

## ✅ Phase 5 — SDK & Project Templates

**Status:** Completed

### Goal
Engine không còn biết project layout.

### Completed
```text
sdk/
templates/
minimal
clean
ddd
mvc
```
Features:
* Project Generator
* Template Loader
* Placeholder Renderer
* Third-party Templates
* Runnable Skeleton

---

## ✅ Phase 6 — Public API Stabilization

**Status:** Completed

### Goal
Chuẩn hóa Public API.

### Completed
Unified API:
```python
engine.dispatch(...)
```
Legacy APIs:
```python
execute()
query()
```
↓
DeprecationWarning
↓
Compatibility Wrapper

Public exports:
```python
from sagittarius_engine import App
```
Architectural Guardrails:
AST Architecture Tests
API Freeze
205 Tests Passing

---

# 🎉 Migration Complete

Đây là cột mốc quan trọng.
Sagittarius **không còn là Clean Architecture framework nữa.**
Nó đã là một **Application Engine**.

---

# Engine Evolution (v1)

Từ đây trở đi **không refactor kiến trúc nữa**.
Chỉ thêm capabilities.

---

# ✅ Phase 7 — Runtime Infrastructure

**Status:** Completed

## Goal
Bổ sung các runtime capability còn thiếu cho desktop apps, trading bots và long-running services.

```text
Runtime Infrastructure
├── HostedServiceManager
├── TaskScheduler
├── TaskManager
├── AsyncRuntime
└── CancellationToken
```

### Hosted Services
```python
class IHostedService:
    start()
    stop()
```
Engine tự quản lý lifecycle.

### Background Task Manager
Ví dụ:
```python
engine.tasks.spawn(...)
```
Có:
* graceful shutdown
* cancellation
* exception propagation

### Scheduler
Ví dụ:
```python
engine.scheduler.every(1).minutes(...)
```
hoặc
```python
@schedule(...)
```

### Async Runtime
Engine quản lý:
* asyncio tasks
* thread tasks
* background workers

Không để user tự tạo thread khắp nơi.

### Acceptance
Trading Bot, Desktop App, Worker, Automation đều chạy được.

---

# 🚧 Phase 8 — CLI & Tooling

Ví dụ:
```bash
sagittarius new
sagittarius run
sagittarius doctor
sagittarius extension list
sagittarius template list
sagittarius test
```
Không đụng kernel.

---

# 🚧 Phase 9 — Documentation & Samples

Ví dụ:
```text
docs/
architecture.md
extensions.md
sdk.md
tutorials/
examples/
```
Ví dụ mẫu:
* Trading Bot
* Binance Client
* PySide Desktop
* REST API
* Worker
* CLI

---

# 🚧 Phase 9.5 — Reference Applications

Ví dụ:
```text
examples/
    trading_bot/
    desktop_pyside/
    crypto_dashboard/
    rest_api/
    worker/
    scheduler/
    websocket/
    plugin_system/
```
Đây không chỉ là example, mà là **proof of architecture**.

Ví dụ Trading Bot:
```text
examples/
    trading_bot/
        app/
        strategies/
        exchanges/
        ui/
        config/
        main.py
```
Người dùng clone, chạy ngay và hoạt động trực quan.

---

# 🚧 Phase 10 — Ecosystem

Ví dụ:
```text
Ecosystem
├── Official
│   ├── sagittarius-binance
│   ├── sagittarius-fastapi
│   └── sagittarius-pyside6
└── Community
    ├── sagittarius-discord
    ├── sagittarius-ai
    └── sagittarius-backtesting
```
Đây là ecosystem lớn mạnh của dự án, độc lập với core kernel.

---

# 🚧 Phase 11 — Stable Release

Kernel Freeze
Semantic Versioning
API Freeze
Performance Benchmarks
Migration Guide
Release Notes
Official Website
PyPI Release
Long-term Support
CI Badge
Coverage
Changelog
