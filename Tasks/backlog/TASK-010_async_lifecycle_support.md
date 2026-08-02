# TASK-010: Async Lifecycle Support

- **Status**: 📝 Planned (Backlog)
- **Priority**: P2 - Medium
- **Category**: Core Architecture / Concurrency
- **Issues Addressed**: Architecture Review Point 2

---

## 🎯 Goal
Provide native support for asynchronous lifecycle hooks (`boot_async`, `shutdown_async`) in `IExtension` and `Lifecycle` to avoid blocking the main thread during heavy I/O initializations.

---

## 📐 Key Enhancements

1. **Async Hooks in IExtension**:
   - Add `boot_async(self, context)` and `shutdown_async(self, context)` to `IExtension` and its implementations.
   - Retain backward compatibility for synchronous `boot` and `shutdown`.
2. **Lifecycle Orchestrator Updates**:
   - Update `EngineLifecycle` to await `boot_async` on extensions that implement it via the `AsyncRuntime`.
   - Prevent blocking the main thread by ensuring heavy initializations (DB connection tests, caching setups) happen inside the async loop.

---

## 📋 Implementation Checklist

- [ ] Add `boot_async` / `shutdown_async` to `IExtension` with default no-op.
- [ ] Modify `EngineLifecycle` to detect and run async hooks safely.
- [ ] Update documentation to guide developers on choosing sync vs async hooks.
- [ ] Add unit tests verifying async boot does not block the thread.
