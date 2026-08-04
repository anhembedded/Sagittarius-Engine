# TASK-017: Production Readiness Hardening

## Background
The Sagittarius Engine has reached a high level of maturity, but an architecture review identified several critical bugs, architectural risks, and bottlenecks that hinder 24/7 production readiness. This task consolidates these issues into a single hardening program.

## Objective
To resolve all identified critical bugs and architectural risks, ensuring the system is robust, memory-safe, secure, and fully decoupled. **Crucially, every issue must include a dedicated test case that reproduces the original failure/risk and guarantees coverage against future regressions.**

---

## Issue Checklist & Specifications

### [ ] 1. System Deadlock in IPC Broker
*   **Issue:** `IPCBroker` distributes events to `subscriber_queues` using `sub_queue.put((event_name, data))` without a timeout or `queue.Full` handling. If a subscriber hangs, the whole IPC bus deadlocks.
*   **Action:** Add a `timeout` (e.g., `0.1`) to the `put()` call. Catch `queue.Full` and gracefully drop the event with a warning log.
*   **Test Case Requirement:** Create a test that deliberately fills a subscriber's queue (or blocks a subscriber) and verifies that the `IPCBroker` does not block indefinitely when broadcasting a new event.

### [ ] 2. Factory Loss in DI Container on Error
*   **Issue:** In `StdContainer.singleton()`, the lazy factory immediately pops the factory from `_factories`. If `_resolve()` fails, the factory is permanently lost.
*   **Action:** Only remove the factory from `_factories` *after* `_resolve()` succeeds and the instance is safely stored in `_instances`.
*   **Test Case Requirement:** Create a test that attempts to resolve a singleton which initially fails (e.g., due to a temporarily missing dependency), then fix the condition, and assert that the second resolution attempt succeeds rather than failing with "Unregistered dependency".

### [ ] 3. Core Middleware Coupled to Extension
*   **Issue:** `TransactionMiddleware` inside the core engine directly imports `ISession` from `sagittarius_engine.extensions.persistence`. This breaks if the persistence extension is not used.
*   **Action:** Move `TransactionMiddleware` out of the core `middleware/` directory and into `extensions/persistence/`. The core should only provide the `IMiddleware` interface.
*   **Test Case Requirement:** Create a test environment (or test case) that initializes the core engine *without* the database extension installed, verifying that no `ImportError` occurs.

### [ ] 4. Deep Hooking into Python Internals
*   **Issue:** `DaemonThreadPoolExecutor` hacks into internal `concurrent.futures.thread` objects (`_worker`, `_threads_queues`) which is brittle across Python versions.
*   **Action:** Remove `DaemonThreadPoolExecutor`. Use the standard `ThreadPoolExecutor` and manage shutdown explicitly via `executor.shutdown(wait=False, cancel_futures=True)`.
*   **Test Case Requirement:** Write a test that validates the `TaskManager` can spawn tasks and shut down cleanly using the standard executor without leaving hanging threads.

### [ ] 5. Memory Leak Risk in Task Manager
*   **Issue:** `_cleanup_old_tasks()` retains up to 50 finished tasks indefinitely. This retains heavy payload closures in memory.
*   **Action:** Implement a TTL (Time-To-Live) mechanism or a strict `max_retained_tasks` configuration via `IConfig`. Clear tasks that exceed the retention policy.
*   **Test Case Requirement:** Write a test that completes a large number of tasks and asserts that they are successfully garbage collected / removed from the task dictionary after the TTL expires or retention limit is hit.

### [ ] 6. Security Flaw in Audit WebSocket
*   **Issue:** `WebsocketBroadcaster` defaults to binding on `0.0.0.0:9999` and broadcasts sensitive system state without authentication.
*   **Action:** Change the default bind address to `127.0.0.1`. Add a basic token authentication mechanism (e.g., verifying a `token=XYZ` query parameter upon connection).
*   **Test Case Requirement:** Write two tests:
    1. Verify connection is rejected if the token is missing or invalid.
    2. Verify successful connection and telemetry broadcast when a valid token is provided.

### [ ] 7. Incomplete Graceful Shutdown
*   **Issue:** `App.stop()` uses sequential `try...except` blocks. If any extension's `stop()` or `dispose()` hangs, the entire shutdown sequence blocks indefinitely.
*   **Action:** Wrap extension shutdown and disposal calls in a timeout mechanism (e.g., `asyncio.wait_for` for async hooks, or threading timeouts for synchronous ones) to guarantee `App.stop()` always completes.
*   **Test Case Requirement:** Create a rogue extension whose `stop()` method contains an infinite loop or `time.sleep(999)`. Write a test verifying that `App.stop()` still completes within a defined timeout threshold despite the rogue extension.

---

## Acceptance Criteria
- [ ] All 7 issues have been addressed in the source code.
- [ ] 7 distinct automated test cases have been added to reproduce the original bugs/risks and verify the fixes.
- [ ] CI pipeline (`lint.ps1` and GitHub Actions) passes with 100% success and 80%+ coverage.
- [ ] No regression in existing functionality.
