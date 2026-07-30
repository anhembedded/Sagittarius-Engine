# Sagittarius Engine - Exception-Case Testing Coverage Report (2026-07-30)

- **Objective**: Identify critical modules requiring exception-case testing improvements
- **Methodology**: Static analysis of exception handling patterns vs existing test coverage
- **Related reports**:
  - [TEST_CASE_ISSUES_2026-07-30.md](TEST_CASE_ISSUES_2026-07-30.md)
  - [ISSUES_TO_FIX_2026-07-30.md](ISSUES_TO_FIX_2026-07-30.md)

---

## Executive Summary

Current state:

- **110 exception tests exist** across the test suite
- However, most focus on **validation errors** and **input edge cases**
- Critical **failure-path scenarios** in kernel/runtime are **under-tested**
- Many broad `except Exception` handlers lack corresponding negative tests

Risk impact:

- Silent failures in production due to swallowed exceptions
- Incomplete rollback during boot failures
- Resource leaks during shutdown edge cases
- Difficult root-cause analysis when partial failures occur

---

## Critical Module Analysis

### 1. kernel/app.py

**Exception Handler Count**: 11 (5 broad catches during stop sequence)

**Location**: [sagittarius_engine/kernel/app.py](../sagittarius_engine/kernel/app.py)

**Current Exception Handling**:

```python
Lines 127-157: App.stop() catches broad exceptions during:
- scheduler.stop()
- hosted_services.stop()
- extension_manager.stop_and_dispose()
- tasks.shutdown()
- async_runtime.stop()
```

**Existing Test Coverage**:

- ✅ Basic stop lifecycle test exists: [tests/test_runtime.py](../tests/test_runtime.py#L235)
- ✅ Stress boot-shutdown cycles: [tests/test_examples.py](../tests/test_examples.py#L39)

**Missing Exception-Case Tests**:

- ❌ Scheduler.stop() raises exception during graceful shutdown
- ❌ Extension.dispose() raises during stop sequence
- ❌ TaskManager.shutdown() times out with active critical tasks
- ❌ AsyncRuntime.stop() fails to cancel pending coroutines
- ❌ Multiple subsystem failures during single stop call

**Priority**: **Critical**

**Suggested Tests**:

```python
test_app_stop__scheduler_raises__other_subsystems_still_stop()
test_app_stop__extension_dispose_fails__no_resource_leak()
test_app_stop__multiple_failures__logs_all_errors()
test_app_stop__already_stopped__idempotent_safe()
```

---

### 2. kernel/bootstrap.py

**Exception Handler Count**: 6 (3 with `nosec B110` broad catches)

**Location**: [sagittarius_engine/kernel/bootstrap.py](../sagittarius_engine/kernel/bootstrap.py)

**Current Exception Handling**:

```python
Lines 39-55: Boot failure triggers rollback with broad exception swallowing
- Rollback calls scheduler.stop(), hosted_services.stop(), async_runtime.stop()
- Each wrapped in bare except Exception without re-raising
```

**Existing Test Coverage**:

- ✅ Extension initialization failure rollback: [tests/test_extension_manager.py](../tests/test_extension_manager.py#L155)

**Missing Exception-Case Tests**:

- ❌ Auto-discovery raises ImportError during boot
- ❌ Extension.start() raises after successful initialize
- ❌ HostedService.start() fails mid-sequence (partial services started)
- ❌ Rollback cleanup itself raises exception
- ❌ Boot fails with scheduler already running (state corruption)

**Priority**: **Critical**

**Suggested Tests**:

```python
test_bootstrap_boot__extension_start_fails__rollback_cleans_initialized()
test_bootstrap_boot__hosted_service_partial_start__rollback_stops_started()
test_bootstrap_boot__rollback_cleanup_fails__logs_error_without_crash()
test_bootstrap_boot__async_runtime_start_fails__no_thread_leak()
```

---

### 3. kernel/extension_manager.py

**Exception Handler Count**: 9

**Location**: [sagittarius_engine/kernel/extension_manager.py](../sagittarius_engine/kernel/extension_manager.py)

**Current Exception Handling**:

```python
Lines 228-286: Extension lifecycle (initialize/start/stop/dispose) with exception handling
Line 97: _try_initialize_available catches exceptions during eager init
Lines 256-286: stop_and_dispose catches exceptions per extension
```

**Existing Test Coverage**:

- ✅ Circular dependency detection: [tests/test_extension_manager.py](../tests/test_extension_manager.py#L133)
- ✅ Missing dependency error: [tests/test_extension_manager.py](../tests/test_extension_manager.py#L116)

**Missing Exception-Case Tests**:

- ❌ Extension.initialize() raises after partial registration
- ❌ Extension.start() fails with optional dependencies present
- ❌ Extension.stop() raises exception during shutdown
- ❌ Extension.dispose() fails to release resources
- ❌ Multiple extensions fail stop simultaneously

**Priority**: **High**

**Suggested Tests**:

```python
test_extension_manager__initialize_raises__rollback_disposes_previous()
test_extension_manager__start_fails__initialized_not_started()
test_extension_manager__stop_raises__dispose_still_called()
test_extension_manager__optional_dep_start_fails__required_deps_unaffected()
```

---

### 4. runtime/tasks/task_manager.py

**Exception Handler Count**: 7

**Location**: [sagittarius_engine/runtime/tasks/task_manager.py](../sagittarius_engine/runtime/tasks/task_manager.py)

**Current Exception Handling**:

```python
Lines 80-88, 157-162, 170-186: Task execution wrapping with broad catches
Line 223: shutdown() with potential hanging critical tasks
```

**Existing Test Coverage**:

- ✅ Basic task spawning: [tests/test_runtime.py](../tests/test_runtime.py#L178)

**Missing Exception-Case Tests**:

- ❌ Critical task raises exception during execution
- ❌ Background task raises during concurrent spawn burst
- ❌ Shutdown with critical tasks that won't terminate within timeout
- ❌ Executor submit() raises (pool exhausted)
- ❌ Task future.result() raises after completion

**Priority**: **High**

**Suggested Tests**:

```python
test_task_manager__critical_task_raises__logged_and_tracked()
test_task_manager__spawn_during_shutdown__rejects_gracefully()
test_task_manager__shutdown_timeout__critical_tasks_force_cancelled()
test_task_manager__executor_full__spawn_raises_clear_error()
```

---

### 5. runtime/hosted/hosted_service_manager.py

**Exception Handler Count**: 4

**Location**: [sagittarius_engine/runtime/hosted/hosted_service_manager.py](../sagittarius_engine/runtime/hosted/hosted_service_manager.py)

**Current Exception Handling**:

```python
Lines 43-48: Service start failure triggers rollback
Lines 78-83: Service stop captures per-service exceptions
```

**Existing Test Coverage**:

- ✅ Hosted service start failure: [tests/test_runtime.py](../tests/test_runtime.py#L71)

**Missing Exception-Case Tests**:

- ❌ Second service start fails after first succeeds (rollback verification)
- ❌ Service.stop() raises during shutdown sequence
- ❌ Multiple services fail stop simultaneously
- ❌ Service start succeeds but immediate health check fails

**Priority**: **Medium**

**Suggested Tests**:

```python
test_hosted_service_manager__second_start_fails__first_stopped()
test_hosted_service_manager__service_stop_raises__others_still_stopped()
test_hosted_service_manager__stop_multiple_errors__all_logged()
```

---

### 6. runtime/scheduler/scheduler.py

**Exception Handler Count**: 2

**Location**: [sagittarius_engine/runtime/scheduler/scheduler.py](../sagittarius_engine/runtime/scheduler/scheduler.py)

**Current Exception Handling**:

```python
Line 165: Scheduled job execution catches exception per job
Line 70: Scheduler thread run loop exception handling
```

**Existing Test Coverage**:

- ✅ Basic scheduling: [tests/test_full_coverage.py](../tests/test_full_coverage.py)

**Missing Exception-Case Tests**:

- ❌ Scheduled job raises exception during execution
- ❌ Job trigger.get_next_run() raises exception
- ❌ Scheduler.stop() called while job is executing
- ❌ Scheduler.add_job() called after scheduler stopped

**Priority**: **Medium**

**Suggested Tests**:

```python
test_scheduler__job_raises__other_jobs_still_run()
test_scheduler__trigger_calculation_fails__job_skipped()
test_scheduler__stop_during_job_execution__waits_completion()
```

---

### 7. runtime/async_runtime/async_runtime.py

**Exception Handler Count**: 1 (broad catch during stop)

**Location**: [sagittarius_engine/runtime/async_runtime/async_runtime.py](../sagittarius_engine/runtime/async_runtime/async_runtime.py)

**Current Exception Handling**:

```python
Lines 60-65: Stop sequence catches exception during asyncio.all_tasks cancellation
```

**Existing Test Coverage**:

- ✅ Basic async runtime: [tests/test_full_coverage.py](../tests/test_full_coverage.py)

**Missing Exception-Case Tests**:

- ❌ Pending coroutines refuse cancellation during stop
- ❌ Loop.stop() called from wrong thread
- ❌ run_coroutine() called after loop stopped
- ❌ Coroutine raises exception during background execution

**Priority**: **Medium**

**Suggested Tests**:

```python
test_async_runtime__stop_with_uncancellable_tasks__force_closed()
test_async_runtime__run_coroutine_after_stop__raises_runtime_error()
test_async_runtime__background_coro_raises__logged_not_crashed()
```

---

### 8. infrastructure/container/std_container.py

**Exception Handler Count**: 2

**Location**: [sagittarius_engine/infrastructure/container/std_container.py](../sagittarius_engine/infrastructure/container/std_container.py)

**Current Exception Handling**:

```python
Lines 187-191: Dependency resolution catches exception during constructor injection
Line 157: Type hint resolution exception handling
```

**Existing Test Coverage**:

- ✅ Circular dependency: [tests/test_edge_cases.py](../tests/test_edge_cases.py#L770)
- ✅ Missing type hint: [tests/test_core.py](../tests/test_core.py#L78)

**Missing Exception-Case Tests**:

- ❌ Factory function raises exception during singleton creation
- ❌ Constructor raises exception after partial dependency injection
- ❌ Concurrent resolve() calls for same singleton factory
- ❌ Type hint resolution fails for complex generic types

**Priority**: **Medium**

**Suggested Tests**:

```python
test_container__factory_raises__dependency_resolution_error_clear()
test_container__constructor_partial_init_fails__cleanup_dependencies()
test_container__concurrent_singleton_resolve__thread_safe()
```

---

### 9. infrastructure/event_bus (all variants)

**Exception Handler Count**: 14 across all bus implementations

**Locations**:

- [sagittarius_engine/infrastructure/event_bus/memory_event_bus.py](../sagittarius_engine/infrastructure/event_bus/memory_event_bus.py)
- [sagittarius_engine/infrastructure/event_bus/thread_pool_event_bus.py](../sagittarius_engine/infrastructure/event_bus/thread_pool_event_bus.py)
- [sagittarius_engine/infrastructure/event_bus/resilient_event_bus.py](../sagittarius_engine/infrastructure/event_bus/resilient_event_bus.py)
- [sagittarius_engine/infrastructure/event_bus/asyncio_event_bus.py](../sagittarius_engine/infrastructure/event_bus/asyncio_event_bus.py)

**Existing Test Coverage**:

- ✅ Handler exception handling: [tests/test_edge_cases.py](../tests/test_edge_cases.py#L112)
- ✅ Resilient bus DLQ: [tests/test_resilient_event_bus.py](../tests/test_resilient_event_bus.py#L40)
- ✅ ThreadPool handler error: [tests/test_thread_pool_event_bus.py](../tests/test_thread_pool_event_bus.py#L28)

**Missing Exception-Case Tests**:

- ❌ ThreadPoolEventBus.shutdown() called while handlers executing
- ❌ ResilientEventBus.reprocess() fails during retry
- ❌ AsyncioEventBus handler raises CancelledError mid-emit
- ❌ MemoryEventBus handler raises during on() registration

**Priority**: **Low** (already has better coverage than others)

**Suggested Tests**:

```python
test_thread_pool_event_bus__shutdown_during_emit__graceful()
test_resilient_event_bus__reprocess_fails_again__dlq_preserved()
```

---

## Priority Summary

### Critical (Immediate)

1. **kernel/app.py** - Stop sequence exception handling
2. **kernel/bootstrap.py** - Boot failure and rollback

### High (Sprint)

1. **kernel/extension_manager.py** - Extension lifecycle failures
2. **runtime/tasks/task_manager.py** - Task execution and shutdown failures

### Medium (Backlog)

1. **runtime/hosted/hosted_service_manager.py** - Service lifecycle
2. **runtime/scheduler/scheduler.py** - Job execution failures
3. **runtime/async_runtime/async_runtime.py** - Async loop edge cases
4. **infrastructure/container/std_container.py** - Resolution failures

### Low (Optional)

1. **infrastructure/event_bus/** - Already has decent coverage

---

## Success Metrics

Current baseline:

- 110 exception tests exist (mostly validation-focused)
- ~15% coverage of critical failure paths

Target after implementation:

- 60-70 new exception-case tests
- ~80% coverage of critical failure paths
- All broad `except Exception` in kernel/runtime backed by negative tests
- Zero silent failures in CI stress scenarios
