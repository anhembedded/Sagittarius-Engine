# ROLE

You are a principal software architect implementing Phase 4 of the Sagittarius Engine.

Previous phases have already transformed Sagittarius into an extensible Application Engine.

The engine now supports IExtension and EngineContext.

This phase introduces a production-grade Extension Dependency Graph and Lifecycle Orchestrator.

Do not redesign the engine.

Do not introduce breaking API changes.

--------------------------------------------------
# OBJECTIVE

Extensions should no longer start in registration order.

Instead they should start according to dependency resolution.

The engine must become responsible for:

- dependency validation
- lifecycle orchestration
- startup ordering
- shutdown ordering

--------------------------------------------------
# CREATE ExtensionDescriptor

Create a metadata object describing an extension.

Suggested fields

name

version

dependencies

optional_dependencies

enabled

priority

author

description

--------------------------------------------------
# DEPENDENCY GRAPH

Build an internal dependency graph.

Example

Metrics

depends on Logger

Logger

depends on Configuration

Engine should calculate

Configuration

↓

Logger

↓

Metrics

using topological sorting.

--------------------------------------------------
# CIRCULAR DEPENDENCIES

Detect circular dependencies.

Example

A

depends on B

B

depends on A

Throw a dedicated exception.

Do not deadlock.

--------------------------------------------------
# MISSING DEPENDENCIES

If an extension depends on another extension that is not registered

raise a clear exception.

Example

Metrics

depends on Logger

Logger missing

↓

ExtensionDependencyError

--------------------------------------------------
# OPTIONAL DEPENDENCIES

Support optional dependencies.

If available

initialize them first.

If missing

continue normally.

--------------------------------------------------
# LIFECYCLE ORCHESTRATOR

ExtensionManager should orchestrate

initialize()

↓

start()

↓

stop()

↓

dispose()

using dependency order.

Shutdown order must be reversed.

--------------------------------------------------
# FAILURE HANDLING

If one extension fails during initialize

previously initialized extensions should be disposed safely.

Do not leave the engine partially initialized.

--------------------------------------------------
# ENGINE EVENTS

Publish lifecycle events.

Examples

ExtensionInitializing

ExtensionStarted

ExtensionStopped

ExtensionDisposed

Use existing EventBus.

--------------------------------------------------
# ENABLE / DISABLE

Allow an extension to be disabled.

Disabled extensions should not participate in lifecycle.

--------------------------------------------------
# COMPATIBILITY

Current

app.use(...)

must continue working.

No API breaking changes.

--------------------------------------------------
# TESTS

Add tests covering

✓ dependency ordering

✓ optional dependency

✓ missing dependency

✓ circular dependency

✓ startup rollback

✓ shutdown ordering

--------------------------------------------------
# ACCEPTANCE CRITERIA

✓ deterministic startup

✓ deterministic shutdown

✓ dependency graph

✓ rollback support

✓ lifecycle events

✓ circular dependency detection

✓ missing dependency detection

✓ all existing tests continue passing

--------------------------------------------------
# OUTPUT

Provide

1. dependency graph architecture

2. lifecycle sequence

3. new classes

4. compatibility report

5. test summary

Do not redesign the kernel.

Do not redesign DI.

Only implement dependency-aware extension orchestration.
Theo mình, đây mới là Phase 4 xứng đáng với một Application Engine.

Đến cuối Phase 4, Sagittarius sẽ có các đặc điểm mà những engine/framework lớn đều có:

Kernel: nhỏ, ổn định, không phụ thuộc business.
Extension System: chuẩn hóa qua IExtension.
EngineContext: composition root.
Dependency Graph: tự động sắp xếp thứ tự khởi động.
Lifecycle Orchestrator: quản lý toàn bộ vòng đời extension với rollback khi lỗi.