# TASK-005: Runtime Concurrency Hardening

- **Status**: 📝 Planned (Backlog)
- **Priority**: P1 - High
- **Category**: Runtime / Concurrency
- **Issues Addressed**: ISSUE-001, ISSUE-002

---

## 🎯 Goal
Eliminate thread-unsafe global monkey patching in `TaskManager` and synchronize `IEventBus` lifecycle cleanup with `App.stop()`.

---

## 📐 Key Enhancements

1. **Safe Worker Thread Initialization (ISSUE-001)**:
   - Remove global `threading.Thread = daemon_thread` assignment in `DaemonThreadPoolExecutor`.
   - Use a thread initializer function or safe thread-factory pattern when instantiating background `ThreadPoolExecutor` worker threads.

2. **EventBus Shutdown Lifecycle Integration (ISSUE-002)**:
   - Define a optional `shutdown()` or `dispose()` contract for event bus implementations.
   - Update `App.stop()` to invoke `event_bus.shutdown()` / `dispose()` if supported.

---

## 📋 Implementation Checklist

- [ ] Refactor `DaemonThreadPoolExecutor` in `sagittarius_engine/runtime/tasks/task_manager.py` to eliminate `threading.Thread` global mutation.
- [ ] Add `shutdown()` support in `App.stop()` for `IEventBus` in `sagittarius_engine/kernel/app.py`.
- [ ] Add unit tests verifying concurrency safety and clean event bus shutdown on `App.stop()`.
