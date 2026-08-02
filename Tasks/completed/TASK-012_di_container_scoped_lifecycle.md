# TASK-012: DI Container Scoped Lifecycle

- **Status**: 📝 Planned (Backlog)
- **Priority**: P2 - Medium
- **Category**: Infrastructure / Dependency Injection
- **Issues Addressed**: Architecture Review Point 4

---

## 🎯 Goal
Extend the `StdContainer` to support "Scoped" lifecycles (e.g., Request Scope) to safely use the Sagittarius Engine in multi-tenant or concurrent web environments (e.g., FastAPI, Flask).

---

## 📐 Key Enhancements

1. **Scope Context Management**:
   - Implement `ContextVars` (PEP 567) or thread-local storage to track dependency resolution per-request or per-session.
2. **Container Methods**:
   - Add `container.scoped(interface, implementation)` to register scoped services.
   - Add `container.create_scope()` to begin a new resolution boundary.
3. **Integration**:
   - Ensure `ISession` / Database adapters can leverage this to create a single Database transaction per web request rather than per-app (Singleton) or per-query (Transient).

---

## 📋 Implementation Checklist

- [ ] Implement `Scoped` registration logic in `StdContainer`.
- [ ] Add `create_scope()` ContextManager for the DI Container.
- [ ] Update `IContainer` interface.
- [ ] Write integration tests validating that two concurrent scopes receive different instances of a scoped dependency, but the same instance within their own scope.
