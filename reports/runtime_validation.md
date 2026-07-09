# Sagittarius Engine - Runtime Validation Report

This report documents the architectural verification, performance metrics, and validation findings of the Sagittarius Engine runtime infrastructure.

---

## 1. Validation Matrix

| Component | Validation Check | Status | Verification Note |
| :--- | :--- | :--- | :--- |
| **Engine Lifecycle** | Topologically boots extensions, hosted services, and scheduler; stops in reverse. | **PASSED** | Verified via lifecycle integration testing and reversed output logs. |
| **Hosted Services** | Starts background loop; triggers rollback of all started services on startup error. | **PASSED** | Verified in `test_hosted_service_lifecycle_and_rollback` stress checks. |
| **Task Manager** | Reuses worker threads; supports asynchronous execution via background loops. | **PASSED** | Cap tracking dict cleans up finished tasks to avoid memory leaks. |
| **Scheduler** | Sleep timeout determined dynamically without busy-waiting. | **PASSED** | Utilizes Condition variables, waking up instantly on shutdown or job insertion. |
| **Cancellation** | Cooperative cancellation via thread-safe CancellationToken. | **PASSED** | Verified in websocket, queue worker, and scheduler loops. |

---

## 2. Micro-Benchmarks (Performance Metrics)

Benchmarks executed on the current Sagittarius Engine host:

- **100 App Boot/Shutdown Cycles**: **0.1111s** total (avg **1.11ms** per cycle).
- **1000 Scheduled Jobs**: **2.25ms** insertion and calculation latency.
- **100 Registered Hosted Services Lifecycle**: **1.32ms** boot/shutdown latency.

---

## 3. Structural Layer Boundaries (AST Guardrails)

The architectural tests inside `tests/test_architecture.py` ensure the following strict dependency boundaries are never breached:
1. `kernel` and `interfaces` have **zero dependencies** on extensions or SDK.
2. `extensions` and `sdk` packages are completely decoupled and have **no cross-package imports**.
3. All dependencies point inward toward the core interfaces and DI container.

---

## 4. Known Constraints & Trade-offs

- **Minute-Aligned CronTrigger**: The basic `CronTrigger` simulation is minute-aligned. It does not parse complex cron syntax (like day of week or day of month).
- **Static Pool Sizing**: The `TaskManager` thread pool size defaults to a static maximum worker limit (20 threads) and does not scale dynamically under peak load.

---

## 5. Future Improvements (v1.1 Candidates)

- **Dynamic Task Sizing**: Adjust thread pool size dynamically according to CPU utilisation and queue depth.
- **Full Cron Parser**: Introduce cron expression parsing (e.g., using `croniter` or writing a lightweight regex parser) to support complex cron schedules.
