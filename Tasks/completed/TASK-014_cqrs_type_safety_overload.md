# TASK-014: CQRS Dispatcher Type Safety (TOutput Resolution)

- **Status**: 📝 Planned (Backlog)
- **Priority**: P3 - Low
- **Category**: Core Architecture / Type Safety
- **Issues Addressed**: Architecture Review Point 1

---

## 🎯 Goal
Restore strict type safety for the `TOutput` of CQRS commands and queries inside `Dispatcher` and `App` without breaking the Mypy Type Bound checking.

---

## 📐 Key Enhancements

1. **Generic Command/Query Binding**:
   - Define a generic base class or interface for Commands/Queries (e.g., `ICommand[TOutput]`) to carry the return type hint.
2. **Dispatcher Overloads / Refactoring**:
   - Refactor `Dispatcher.execute()` and `Dispatcher.query()` to use `typing.overload` or proper Generic inference based on the `command_class` passed in, allowing Mypy to automatically infer the return type.
   - Remove the `-> Any` fallback used in the IKernelContext migration and replace it with strict bounds.

---

## 📋 Implementation Checklist

- [ ] Create `ICommand[TResult]` and `IQuery[TResult]` base generic protocols.
- [ ] Update `App.execute`, `App.query`, `Dispatcher.execute`, `Dispatcher.query` signatures.
- [ ] Implement `@overload` if needed to map Command types to Output types.
- [ ] Verify `mypy` infers types correctly in Caller code (e.g., `result = app.execute(Cmd())` resolves `result` type).
