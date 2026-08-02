# TASK-013: Engine Context God Object Prevention

- **Status**: 📝 Planned (Backlog)
- **Priority**: P3 - Low
- **Category**: Core Architecture / Clean Architecture
- **Issues Addressed**: Architecture Review Point 5

---

## 🎯 Goal
Prevent `IEngineContext` from accumulating too many utility properties (event_bus, config, container, app, etc.) and naturally evolving into a God Object Anti-Pattern.

---

## 📐 Key Enhancements

1. **Context Interface Segregation**:
   - Continue the work started in TASK-008 to break down `IEngineContext` into smaller, read-only interfaces based on the Interface Segregation Principle (ISP).
2. **Strict Injection over Context Passing**:
   - For user-facing modules and handlers, enforce relying on Dependency Injection (via `__init__`) instead of injecting the monolithic `IEngineContext`.
   - The Context should ONLY be used during the Bootstrap and Extension initialization phase, not in business logic layers.

---

## 📋 Implementation Checklist

- [ ] Audit usage of `IEngineContext` in business logic or handlers and refactor to use standard DI.
- [ ] Restrict extension developers from modifying the Context dynamically.
- [ ] Add architectural linting rules (via tools like `import-linter` or custom AST checks) to ensure `IEngineContext` is not imported inside `domain` or `application` layers.
