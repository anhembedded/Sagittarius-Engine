# TASK-011: Strict Extension Adapter Typing

- **Status**: 📝 Planned (Backlog)
- **Priority**: P3 - Low
- **Category**: Core Architecture / Robustness
- **Issues Addressed**: Architecture Review Point 3

---

## 🎯 Goal
Eliminate duck-typing (`hasattr`) when registering legacy objects in `ExtensionManager` and enforce rigorous interface contracts for extensions and modules.

---

## 📐 Key Enhancements

1. **Remove Duck-Typing Fallback**:
   - In `ExtensionManager.register`, remove the `hasattr(extension_or_module, "register")` check.
   - Enforce that all registered objects MUST inherit from `IExtension` or `IModule`.
2. **Adapter Pattern Refinement**:
   - If backward compatibility is needed for external codebases, provide an explicit `LegacyModuleAdapter` builder that users must manually wrap around their objects, rather than the engine silently guessing types.

---

## 📋 Implementation Checklist

- [ ] Remove `hasattr` block in `sagittarius_engine.kernel.extension_manager`.
- [ ] Update `mypy` configurations if any `cast` calls can be safely removed.
- [ ] Fix any failing unit tests that relied on duck-typing mocks.
- [ ] Ensure clear `TypeError` exceptions are raised if an invalid object is registered.
