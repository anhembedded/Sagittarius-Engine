# TASK-008: Context Decoupling Program

- **Status**: 📝 Planned (Backlog)
- **Priority**: P2 - Medium
- **Category**: Core Architecture / Service Boundaries
- **Issues Addressed**: ISSUE-007

---

## 🎯 Goal
Decouple `EngineContext` into narrow capability interfaces (e.g. `ITaskCapability`, `ISchedulingCapability`) to prevent service locator pattern anti-patterns and improve modularity.

---

## 📐 Key Enhancements

1. **Capability Interface Extraction (ISSUE-007)**:
   - Define explicit capability interfaces (`ITaskCapability`, `ISchedulingCapability`, `IEventCapability`, `ILoggingCapability`) in `sagittarius_engine.interfaces`.
   - Update `EngineContext` to implement these capability interfaces while restricting unneeded mutable state setters.

2. **Extension Boundary Decoupling**:
   - Update extension interfaces and consumers to depend on specific capability interfaces rather than full monolithic `EngineContext`.

---

## 📋 Implementation Checklist

- [ ] Define `ITaskCapability`, `ISchedulingCapability`, etc. in `sagittarius_engine/interfaces/`.
- [ ] Implement capability interfaces on `EngineContext` in `sagittarius_engine/kernel/context.py`.
- [ ] Refactor extension initialization and unit tests to accept narrow capability contracts.
