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

# ✅ Phase 8 — Reference Applications

**Status:** Completed

### Goal
Xây dựng bộ ứng dụng mẫu thực tế (Reference Applications) để kiểm thử và chứng minh kiến trúc Sagittarius Engine.

### Completed
* **`trading_bot`**: Ứng dụng mẫu long-running service có cấu trúc thư mục modular (`app/`), exchange mock (`IHostedService`), và spawning order execution.
* **`desktop`**: Mô phỏng event loop tích hợp với thread-safe task manager và events notification để cập nhật giao diện mà không bị khóa cứng vào PySide6.
* **`rest_api`**: Server HTTP bằng standard library dùng dispatcher và DI container.
* **`worker`**: Background queue processor chạy liên tục và hỗ trợ cooperative cancellation.
* **`websocket`**: Client websocket mô phỏng có heartbeat loop, auto-reconnect backoff và cancellation token.
* **`plugin_system`**: Kiểm thử Topological Sort của 3 tầng extension phụ thuộc (`Metrics` -> `Trading` -> `Dashboard`).
* **`benchmark_runtime.py` & `runtime_validation.md`**: Bổ sung bộ benchmark đo hiệu năng (boot, scheduler, hosted services) và báo cáo xác thực kiểm chứng kiến trúc.

# 🚧 Phase 9 — CLI & Developer Experience

Mục tiêu không phải thêm tính năng vào kernel (đã đóng băng), mà là giúp người dùng sử dụng engine dễ dàng hơn.

Ví dụ các câu lệnh CLI:
```bash
sagittarius new <template_name>
sagittarius run
sagittarius doctor
sagittarius benchmark
sagittarius template list
sagittarius extension list
sagittarius graph
```

* `sagittarius graph`: Hiển thị sơ đồ dependency graph (App -> Extensions -> Hosted Services).
* Hoàn toàn không đụng vào kernel.

---

# 🚧 Phase 10 — Documentation

Viết tài liệu theo cấu trúc học tập và thực hành:
```text
Getting Started -> Concepts -> Tutorial -> Advanced -> API
```

Các chủ đề tài liệu cốt lõi:
* `getting_started.md`
* `runtime.md`
* `extensions.md`
* `scheduler.md`
* `hosted_services.md`
* `event_bus.md`
* `desktop.md`
* `trading_bot.md`

**Quy tắc tài liệu**: Mỗi API phải trả lời được 3 câu hỏi:
1. **Why?** (Tại sao tồn tại?)
2. **When?** (Khi nào dùng?)
3. **When NOT?** (Khi nào không nên dùng?)

---

# 🚧 Phase 11 — Official Ecosystem

Xây dựng các adapter/ecosystem packages độc lập để kiểm chứng runtime capabilities:

1. **`sagittarius-binance`**: Chứng minh Async Runtime, Hosted Services, Scheduler, Event Bus, và Task Manager.
2. **`sagittarius-pyside6`**: Chứng minh Desktop Runtime (luồng GUI mượt mà, delegating tasks sang TaskManager, nhận update qua EventBus).
3. **`sagittarius-fastapi`**: Chứng minh DI, Dispatcher, Hosted Services, và Configuration.
4. **`sagittarius-redis`**: Adapter lưu trữ và giao tiếp phân tán.

---

# 🚧 Phase 12 — Stable Release v1.0

Chuẩn bị sẵn sàng cho production release:
* **CI/CD**: Tự động test trên Linux, Windows, macOS qua Python 3.10, 3.11, 3.12, 3.13.
* **Benchmarks**: Chạy kiểm tra Boot Time, Memory, Scheduler, Task Manager, Hosted Service.
* **Coverage**: Duy trì kiểm thử code coverage > 90%.
* **Release deliverables**: Release Notes, Migration Guide, PyPI publication, website chính thức.

---

# 🚀 Sau v1.0 — Production Verification & Evolution

* **Đóng băng hoàn toàn core kernel**: Không tự đoán tính năng mới, để nhu cầu của hệ sinh thái và người dùng thực tế dẫn dắt (ví dụ: Retry Policy, Circuit Breaker, Distributed Scheduler).
* **Ứng dụng thực tế**: Xây dựng một dự án thực tế hoàn chỉnh (ví dụ: *Sagittarius Trading Bot* kết nối Binance, PySide6, SQLite, Indicators, Risk Manager, Backtesting) chạy liên tục trong nhiều tuần để kiểm chứng độ ổn định của Application Engine trong môi trường production thực sự.
