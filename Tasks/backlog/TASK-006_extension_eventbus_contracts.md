# TASK-006: Extension and Event Bus Contract Consistency

- **Status**: 📝 Planned (Backlog)
- **Priority**: P1 - High
- **Category**: Architecture / Event Bus & Extensions
- **Issues Addressed**: ISSUE-003, ISSUE-004, ISSUE-005

---

## 🎯 Goal
Align extension dependency resolution rules so optional dependencies do not block eager initialization, clean up handler encapsulation in `ThreadPoolEventBus`, and enforce a unified decorator pattern in `ResilientEventBus`.

---

## 📐 Key Enhancements

1. **Optional Dependency Semantics (ISSUE-003)**:
   - Ensure missing or uninitialized optional dependencies in `ExtensionManager._try_initialize_available()` do not block extension initialization unless the optional dependency is explicitly present in registered extensions.

2. **ResilientEventBus Architecture Alignment (ISSUE-004)**:
   - Eliminate duplicate registration paths between local handler tuple and `inner_bus`.
   - Implement consistent delegation or standalone handler tracking.

3. **Public Handler Access API (ISSUE-005)**:
   - Eliminate direct access to `_inner_bus._handlers` in `ThreadPoolEventBus`.
   - Expose a public accessor method (e.g. `get_handlers()`) on `MemoryEventBus` / `IEventBus`.

---

## 📋 Implementation Checklist

- [ ] Fix dependency checks in `ExtensionManager._try_initialize_available()` in `sagittarius_engine/kernel/extension_manager.py`.
- [ ] Add `get_handlers(event_name)` to `MemoryEventBus` / `IEventBus` and update `ThreadPoolEventBus`.
- [ ] Refactor `ResilientEventBus` registration and invocation logic in `sagittarius_engine/infrastructure/event_bus/resilient_event_bus.py`.
- [ ] Add unit tests covering optional dependency graphs and event handler dispatch behavior.
