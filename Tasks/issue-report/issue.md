# Sagittarius Engine - Issues To Fix (2026-07-30)
 
- Source: [ARCHITECTURE_REVIEW_REPORT_2026-07-30.md](ARCHITECTURE_REVIEW_REPORT_2026-07-30.md)
- Objective: consolidate high-impact issues to improve OSS and enterprise readiness.
 
---
 
## 1) Critical
 
### ISSUE-001: Global monkey patch of threading.Thread
- Severity: Critical
- Location: [sagittarius_engine/runtime/tasks/task_manager.py](../sagittarius_engine/runtime/tasks/task_manager.py)
- Evidence:
  - The monkey patch inside `_adjust_thread_count()` can affect the entire process.
- Risks:
  - Unintended side effects in thread creation across unrelated modules.
  - Hard-to-debug race conditions in production.
- Recommended fix:
  - Remove global monkey patching.
  - Use a safe executor/thread-factory approach without mutating global threading state.
- Acceptance criteria:
  - No remaining `threading.Thread = ...` assignments in the codebase.
  - Concurrency unit tests pass on Linux and Windows.
  - No regression in `TaskManager.spawn()` behavior.
 
---
 
## 2) High
 
### ISSUE-002: Event bus lifecycle is not synchronized with App.stop()
- Severity: High
- Location:
  - [sagittarius_engine/kernel/app.py](../sagittarius_engine/kernel/app.py)
  - [sagittarius_engine/infrastructure/event_bus/thread_pool_event_bus.py](../sagittarius_engine/infrastructure/event_bus/thread_pool_event_bus.py)
- Risks:
  - Event bus thread pools may survive after app shutdown.
  - Resource leakage and non-clean shutdown in long-running workloads.
- Recommended fix:
  - Define a shared lifecycle contract for runtime resources (for example `shutdown()` or `dispose()`).
  - Ensure `App.stop()` explicitly shuts down the event bus when supported.
- Acceptance criteria:
  - `App.stop()` reliably releases event bus resources.
  - Shutdown idempotency tests pass.
 
### ISSUE-003: optional_dependencies behaves like required dependencies during eager initialization
- Severity: High
- Location: [sagittarius_engine/kernel/extension_manager.py](../sagittarius_engine/kernel/extension_manager.py)
- Risks:
  - Unexpected extension initialization ordering.
  - Unnecessary startup delays.
- Recommended fix:
  - Align dependency semantics:
    - Required dependencies remain mandatory.
    - Optional dependencies influence order only when present, and must not block initialization.
- Acceptance criteria:
  - Missing optional dependencies do not block initialization.
  - Dependency graph tests pass for both optional-present and optional-absent cases.
 
---
 
## 3) Medium
 
### ISSUE-004: ResilientEventBus uses split handler registration paths
- Severity: Medium
- Location: [sagittarius_engine/infrastructure/event_bus/resilient_event_bus.py](../sagittarius_engine/infrastructure/event_bus/resilient_event_bus.py)
- Risks:
  - Hard-to-predict behavior between local handlers and inner bus handlers.
  - Increased chance of duplicate or divergent event flows.
- Recommended fix:
  - Choose one consistent architecture:
    - Either a true decorator model (delegate emit to inner bus with retry wrapper),
    - Or a standalone resilient bus (do not mirror registrations into inner bus).
- Acceptance criteria:
  - Tests confirm no duplicate callback execution.
  - `on/off/emit/reprocess` behavior is consistent and documented.
 
### ISSUE-005: ThreadPoolEventBus depends on private _handlers state
- Severity: Medium
- Location: [sagittarius_engine/infrastructure/event_bus/thread_pool_event_bus.py](../sagittarius_engine/infrastructure/event_bus/thread_pool_event_bus.py)
- Risks:
  - Encapsulation violation.
  - Fragility if MemoryEventBus changes internals.
- Recommended fix:
  - Introduce a safe public handler snapshot API, or refactor composition to avoid private state access.
- Acceptance criteria:
  - No direct access to `_inner_bus._handlers`.
  - Event delivery regression tests pass.
 
### ISSUE-006: Broad except Exception blocks swallow important failures
- Severity: Medium
- Representative locations:
  - [sagittarius_engine/kernel/bootstrap.py](../sagittarius_engine/kernel/bootstrap.py)
  - [sagittarius_engine/runtime/async_runtime/async_runtime.py](../sagittarius_engine/runtime/async_runtime/async_runtime.py)
  - [sagittarius_engine/kernel/extension_manager.py](../sagittarius_engine/kernel/extension_manager.py)
- Risks:
  - Reduced production diagnosability.
  - Slower root-cause analysis.
- Recommended fix:
  - Catch narrower exception types where possible.
  - Standardize telemetry and structured error reporting for rollback/failure paths.
- Acceptance criteria:
  - Fewer broad catches in critical kernel/runtime paths.
  - Error logs include execution context (component, phase, optional correlation id).
 
### ISSUE-007: EngineContext is too broad and risks service-locator drift
- Severity: Medium
- Location: [sagittarius_engine/kernel/context.py](../sagittarius_engine/kernel/context.py)
- Risks:
  - High coupling, reduced scalability for large teams.
  - Weaker capability-boundary enforcement.
- Recommended fix:
  - Extract narrower capability interfaces for extensions and hosted services.
  - Reduce runtime mutability (limit mutable setters where unnecessary).
- Acceptance criteria:
  - At least two capability interfaces are adopted (for example TaskCapability and SchedulingCapability).
  - New extensions do not require full EngineContext dependency.
 
---
 
## 4) Low (OSS polish)
 
### ISSUE-008: Documentation links still use placeholder your-repo
- Severity: Low
- Representative location: [docs/advanced/architecture.md](../docs/advanced/architecture.md)
- Risks:
  - Reduced trust for open-source users.
- Recommended fix:
  - Replace all documentation footer links with the real repository URL.
- Acceptance criteria:
  - No remaining `your-repo` strings in docs.
 
### ISSUE-009: Missing dedicated CONTRIBUTING guide
- Severity: Low
- Location: repository root
- Risks:
  - Harder onboarding for new contributors.
  - Inconsistent pull request quality.
- Recommended fix:
  - Add `CONTRIBUTING.md` with branch strategy, style rules, test gates, and docs gates.
- Acceptance criteria:
  - `CONTRIBUTING.md` exists and is linked from [readme.md](../readme.md).
 
---
 
## 5) Recommended Execution Order (ROI)
 
1. ISSUE-001
2. ISSUE-002
3. ISSUE-003
4. ISSUE-005
5. ISSUE-004
6. ISSUE-006
7. ISSUE-007
8. ISSUE-008
9. ISSUE-009
 
---
 
## 6) Backlog Mapping
 
- TASK-005: Runtime Concurrency Hardening (ISSUE-001, ISSUE-002)
- TASK-006: Extension and Event Bus Contract Consistency (ISSUE-003, ISSUE-004, ISSUE-005)
- TASK-007: Kernel Reliability and OSS Readiness (ISSUE-006, ISSUE-008, ISSUE-009)
- TASK-008: Context Decoupling Program (ISSUE-007)
 

