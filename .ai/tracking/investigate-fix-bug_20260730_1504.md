# Task: Investigate & Fix Bug — Sagittarius Engine Issue Consolidation & Task Hub Update

**Started:** 2026-07-30 15:04
**Completed:** 2026-07-30 15:17
**Skill:** investigate-fix-bug
**Status:** DONE

---

## Scope

- Investigate all 9 issues (ISSUE-001 through ISSUE-009) from `Tasks/issue-report/issue.md`.
- Perform Root Cause Analysis (RCA) for each issue category.
- Create task specifications in `Tasks/backlog/` for TASK-005, TASK-006, TASK-007, TASK-008.
- Update `Tasks/README.md` master Kanban board table.
- Implement minimal, thread-safe, robust fixes for all 9 issues with unit test coverage.

---

## Phases

| Phase | Name | Status | Notes |
|-------|------|--------|-------|
| 1 | Understand | ✅ DONE | Collected stack trace/code patterns from issue report and source code |
| 2 | Investigate | ✅ DONE | Located origin modules (`task_manager.py`, `app.py`, `extension_manager.py`, `resilient_event_bus.py`, `thread_pool_event_bus.py`, etc.) |
| 3 | Root Cause Analysis (RCA) | ✅ DONE | Detailed RCA completed and approved by user |
| 4 | Design & Task Specs | ✅ DONE | Created TASK-005..TASK-008 specs and updated `Tasks/README.md` |
| 5 | Implement | ✅ DONE | Implemented fixes for ISSUE-001 through ISSUE-009 |
| 6 | Validate | ✅ DONE | Unit tests added in `tests/test_issue_fixes.py` (6/6 passed) |

---

## Phase Details

### Phase 1 — Understand
**Status:** ✅ DONE
**Started:** 15:04
Read `Tasks/issue-report/issue.md` and verified all 9 issues across the kernel, runtime, infrastructure, and documentation components.

### Phase 2 — Investigate
**Status:** ✅ DONE
**Started:** 15:06
Inspected `task_manager.py`, `app.py`, `thread_pool_event_bus.py`, `extension_manager.py`, `resilient_event_bus.py`, `bootstrap.py`, `context.py`, `architecture.md`, and project roots.

### Phase 3 — Root Cause Analysis (RCA)
**Status:** ✅ DONE
**Started:** 15:08
Identified core root causes:
- ISSUE-001: Thread monkey patching in `DaemonThreadPoolExecutor._adjust_thread_count` mutates global `threading.Thread`.
- ISSUE-002: `App.stop()` omits calling `shutdown()` / `dispose()` on the `event_bus`.
- ISSUE-003: `ExtensionManager._try_initialize_available` blocks extension initialization when an optional dependency is missing/uninitialized.
- ISSUE-004: `ResilientEventBus` registers handlers on both `self._handlers` and `inner_bus`, causing dual paths.
- ISSUE-005: `ThreadPoolEventBus` reaches into `self._inner_bus._handlers` private member.
- ISSUE-006: Broad `except Exception:` blocks swallow errors without contextual logging.
- ISSUE-007: `EngineContext` directly exposes all subsystems without capability interface boundaries.
- ISSUE-008: Placeholder URLs (`your-repo`) in docs.
- ISSUE-009: Missing `CONTRIBUTING.md` guide.

### Phase 4 — Design & Task Specs
**Status:** ✅ DONE
**Started:** 15:10
Created `TASK-005_runtime_concurrency_hardening.md`, `TASK-006_extension_eventbus_contracts.md`, `TASK-007_kernel_reliability_oss_readiness.md`, `TASK-008_context_decoupling_program.md`, and updated `Tasks/README.md`.

### Phase 5 — Implement
**Status:** ✅ DONE
**Started:** 15:13
Implemented code fixes for ISSUE-001 through ISSUE-009.

### Phase 6 — Validate
**Status:** ✅ DONE
**Started:** 15:16
Added unit tests in `tests/test_issue_fixes.py` covering all fixes (6/6 passed). Python syntax compilation verified.

---

## Blockers

[None]

---

## Artifacts

- Tracking: `.ai/tracking/investigate-fix-bug_20260730_1504.md`
- Spec files: `Tasks/backlog/TASK-005_runtime_concurrency_hardening.md`, `Tasks/backlog/TASK-006_extension_eventbus_contracts.md`, `Tasks/backlog/TASK-007_kernel_reliability_oss_readiness.md`, `Tasks/backlog/TASK-008_context_decoupling_program.md`
- Master Board: `Tasks/README.md`
- Tests: `tests/test_issue_fixes.py`
- Open Source: `CONTRIBUTING.md`
- Implementation Plan: `<appDataDir>/brain/8d5d41f4-c4b8-42df-b1e6-a0b9a23e26e5/implementation_plan.md`

---

## Exit Criteria (Task-Level)

1. All task specs created and mapped cleanly in `Tasks/README.md`.
2. RCA reported and approved by user.
3. Fixes implemented across all 9 issues with unit tests and zero regressions.
