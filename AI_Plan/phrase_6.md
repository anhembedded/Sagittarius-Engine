Mình sẽ **không làm CLI trước**.

Đây là điểm mình khác với nhiều roadmap.

CLI chỉ là **UI của Engine**.

Nếu API chưa stable thì CLI sẽ phải sửa liên tục.

Nên theo mình thứ tự đúng là:

```text
Kernel ✅

↓

Extension Runtime ✅

↓

SDK ✅

↓

API Freeze  ← NEXT

↓

CLI

↓

Documentation

↓

v1.0
```

---

# Phase 6 — Public API Stabilization & Deprecation Policy

Đây là phase cuối cùng đụng vào code core.

Sau phase này:

* Kernel API Freeze
* Extension API Freeze
* SDK API Freeze

Sau đó sẽ không đổi API nữa cho tới v2.

---

# Prompt

```text
# ROLE

You are a Principal Software Architect responsible for preparing Sagittarius Engine for its first stable public release.

Previous phases have successfully transformed Sagittarius from a Clean Architecture framework into a modular Application Engine.

The kernel, EngineContext, Extension Runtime, SDK, and Template System are considered feature complete.

This phase is NOT about adding features.

This phase focuses entirely on stabilizing the public API.

--------------------------------------------------
# OBJECTIVE

Freeze the public API.

Identify every public-facing API.

Classify them as:

- Stable
- Experimental
- Deprecated
- Internal

The goal is to guarantee long-term backwards compatibility.

--------------------------------------------------
# PUBLIC API AUDIT

Review every exported class, function and namespace.

Determine whether it belongs to:

Kernel API

Extension API

SDK API

Internal implementation

Only public APIs should be exported.

Anything internal should be hidden.

--------------------------------------------------
# CREATE PUBLIC API SURFACE

Each package should explicitly define its public interface.

Examples:

__init__.py

__all__

Documented exports

Avoid leaking implementation details.

--------------------------------------------------
# API CLASSIFICATION

Every public API should have one status.

Stable

Experimental

Deprecated

Internal

Examples

App

Stable

EngineContext

Stable

Dispatcher

Stable

ExtensionManager

Stable

Bootstrap

Internal

ModuleLoader

Internal

Legacy CQRS imports

Deprecated

--------------------------------------------------
# DEPRECATION POLICY

Introduce a consistent deprecation policy.

Every deprecated API must:

emit DeprecationWarning

provide migration guidance

remain functional

Examples

app.execute(...)

↓

warnings.warn(
    "... is deprecated, use dispatch()",
    DeprecationWarning,
)

↓

return dispatch(...)

Do not remove deprecated APIs.

--------------------------------------------------
# API ALIASES

Where appropriate, introduce new preferred APIs while preserving compatibility.

Example

execute()

↓

dispatch()

query()

↓

dispatch()

The old methods should become compatibility wrappers.

Do not break existing applications.

--------------------------------------------------
# EXPORT CLEANUP

Avoid exposing implementation classes.

Examples

Bootstrap

LifecycleCoordinator

InternalDescriptors

DependencyResolver

should not appear as public API unless necessary.

--------------------------------------------------
# PACKAGE STRUCTURE

Review every package.

Ensure users naturally import from

sagittarius_engine

instead of deep internal modules.

Preferred

from sagittarius_engine import App

from sagittarius_engine import EngineContext

Avoid

from sagittarius_engine.kernel.bootstrap.internal...

--------------------------------------------------
# DOCUMENTATION

Generate API documentation annotations.

Every Stable API should include:

Purpose

Parameters

Return values

Example usage

Version introduced

Every Deprecated API should include:

Reason

Replacement

Removal target version

--------------------------------------------------
# VERSIONING

Prepare the project for Semantic Versioning.

Define

Stable API

Experimental API

Internal API

Future compatibility expectations

--------------------------------------------------
# TESTS

Add compatibility tests ensuring:

old APIs still work

new APIs work

deprecation warnings are emitted

public exports resolve correctly

no internal modules are accidentally exposed

--------------------------------------------------
# DO NOT CHANGE

Do NOT redesign the kernel.

Do NOT redesign the extension runtime.

Do NOT redesign EngineContext.

Do NOT redesign SDK.

Do NOT introduce new runtime features.

Only stabilize and document the public API.

--------------------------------------------------
# ACCEPTANCE CRITERIA

✓ Every public API is explicitly classified.

✓ Stable API is frozen.

✓ Internal APIs are hidden.

✓ Deprecated APIs emit warnings.

✓ Compatibility wrappers work.

✓ Existing applications remain functional.

✓ Existing tests continue passing.

✓ New compatibility tests are added.

--------------------------------------------------
# OUTPUT

Provide:

1. Public API inventory.

2. Stable API list.

3. Experimental API list.

4. Deprecated API list.

5. Internal-only components.

6. Migration guide.

7. Compatibility report.

Do not implement CLI.

Do not redesign architecture.

Only stabilize the Sagittarius Engine public API for the first stable release.
```

---

## Tuy nhiên, mình còn đề xuất **một Phase 6.5** mà mình nghĩ cực kỳ đáng giá.

Đó là **Architecture Enforcement**.

Hiện tại engine đã đẹp, nhưng ai đó sau này có thể vô tình viết:

```python
kernel/
    import extensions.sqlalchemy
```

và toàn bộ kiến trúc sẽ bị phá.

Nên thêm các **architectural tests** để bảo vệ thiết kế:

* `kernel` **không được import** `extensions`.
* `kernel` **không được phụ thuộc** `sdk`.
* `extensions` **được phép phụ thuộc** `kernel`.
* `sdk` **được phép phụ thuộc** `kernel`, nhưng `kernel` không phụ thuộc `sdk`.
* Phát hiện **circular dependency** giữa package.
* Kiểm tra chỉ các API được khai báo mới được export.

Đây là những "guardrails" rất nhiều framework lớn sử dụng để giữ kiến trúc sạch trong nhiều năm. Theo mình, nếu Sagittarius hướng tới một engine lâu dài thì bước này còn quan trọng hơn cả CLI.
