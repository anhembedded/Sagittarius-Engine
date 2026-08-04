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

---

## 🤖 AI Execution Guide
If you are an AI assistant executing this task:
1. **Goal**: Your core objective is to prevent `EngineContext` from becoming a monolithic "God Object". Do this by segregating its responsibilities into fine-grained capability interfaces (e.g., `ITaskCapability`, `ISchedulingCapability`) in `sagittarius_engine/interfaces/`.
2. Update `EngineContext` to inherit and implement these narrow interfaces. Update extensions to type-hint against these specific capabilities instead of the broad `IEngineContext` or `EngineContext`.
3. **Tracking Update (CRITICAL):** Once all code changes are complete and verified, you must move this file (`TASK-008_context_decoupling_program.md`) from `Tasks/backlog/` to `Tasks/completed/`.
4. Open `Tasks/README.md`, remove TASK-008 from the **🔵 Backlog** table, add it to the **🟢 Completed** table with today's date, and update the Directory Layout tree to reflect the file move.
