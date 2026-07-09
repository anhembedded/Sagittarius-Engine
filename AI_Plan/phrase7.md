Mình rất thích roadmap mới. Theo mình **Phase 7 là phase cuối cùng đụng vào Engine Core**. Sau phase này thì Kernel gần như "feature complete".

Tuy nhiên mình muốn chỉnh một chút triết lý.

**Đừng xây Runtime Infrastructure theo hướng Trading Bot.**

Hãy xây theo hướng:

> **General-purpose Host Runtime**

Tức là giống .NET Generic Host, ASP.NET Core Host hay Java Spring Boot Runtime.

Trading Bot chỉ là một consumer của runtime đó.

---

# Prompt Phase 7 — Runtime Infrastructure

```text
# ROLE

You are a Principal Software Architect implementing Phase 7 of the Sagittarius Engine roadmap.

Previous phases have successfully transformed Sagittarius into a modular Application Engine.

The architecture is now considered stable.

DO NOT redesign the kernel.

DO NOT redesign the Extension System.

DO NOT redesign EngineContext.

DO NOT redesign Dispatcher.

DO NOT redesign Middleware.

DO NOT redesign SDK.

This phase only adds missing runtime capabilities required by modern long-running applications.

--------------------------------------------------
# OBJECTIVE

Transform Sagittarius into a production-ready runtime host.

The runtime should support applications such as:

- Trading Bots
- Desktop Applications
- Workers
- Automation Services
- Background Daemons
- Data Pipelines

without requiring users to manually manage threads,
asyncio loops,
timers,
or service lifecycle.

The runtime must remain generic.

It must NOT contain trading-specific concepts.

--------------------------------------------------
# DESIGN PRINCIPLE

Runtime Infrastructure provides execution capabilities.

Applications provide business logic.

Extensions integrate technologies.

Never mix these responsibilities.

--------------------------------------------------
# CREATE RUNTIME PACKAGE

Introduce a dedicated runtime package.

Suggested structure

runtime/

    hosted/

        hosted_service.py

        hosted_service_manager.py

    tasks/

        task_manager.py

        cancellation_token.py

        background_task.py

    scheduler/

        scheduler.py

        cron_trigger.py

        interval_trigger.py

    async_runtime/

        async_runtime.py

--------------------------------------------------
# HOSTED SERVICES

Introduce IHostedService.

Example

class IHostedService:

    def start(context):
        ...

    def stop(context):
        ...

Hosted services represent long-running engine components.

Examples

Price Feed

Websocket Client

Background Sync

Heartbeat

Cache Refresher

Hosted services should automatically participate in engine lifecycle.

--------------------------------------------------
# HOSTED SERVICE MANAGER

Create HostedServiceManager.

Responsibilities

- register services

- start all services

- stop all services

- lifecycle ordering

- graceful shutdown

- exception aggregation

EngineContext should expose

context.hosted_services

--------------------------------------------------
# TASK MANAGER

Create a unified TaskManager.

Responsibilities

spawn()

cancel()

cancel_all()

wait()

track()

report failures

Support

threads

asyncio

future extensibility

Do not expose raw threading APIs.

Example

task = engine.tasks.spawn(...)

--------------------------------------------------
# CANCELLATION TOKEN

Create CancellationToken.

Requirements

thread-safe

cooperative cancellation

timeout support

status inspection

Tasks should periodically check

token.is_cancelled()

--------------------------------------------------
# ASYNC RUNTIME

Provide AsyncRuntime abstraction.

Responsibilities

manage asyncio loop

submit coroutine

shutdown loop

await tasks

Do not require users to manually create loops.

--------------------------------------------------
# SCHEDULER

Create a lightweight scheduler.

Support

fixed interval

cron expression (basic abstraction only)

delayed execution

recurring execution

Examples

engine.scheduler.every(minutes=1)

engine.scheduler.after(seconds=10)

Future scheduler implementations may replace this.

Keep abstraction clean.

--------------------------------------------------
# ENGINE LIFECYCLE

Integrate Runtime Infrastructure into Engine lifecycle.

Boot sequence

Container

↓

Extensions

↓

Hosted Services

↓

Scheduler

↓

Application Ready

Shutdown sequence

Scheduler

↓

Hosted Services

↓

Extensions

↓

Kernel

Graceful shutdown is mandatory.

--------------------------------------------------
# FAILURE HANDLING

If a Hosted Service fails during startup

Rollback previously started services.

Do not leave background threads running.

Scheduler failures must not crash unrelated services.

Task exceptions should be propagated to TaskManager.

--------------------------------------------------
# THREAD SAFETY

All runtime infrastructure must be thread-safe.

Protect shared collections.

Avoid race conditions.

Avoid deadlocks.

--------------------------------------------------
# OBSERVABILITY

Publish runtime events.

Examples

HostedServiceStarted

HostedServiceStopped

TaskStarted

TaskCompleted

TaskFailed

SchedulerStarted

SchedulerStopped

Use existing EventBus.

Do not create another event mechanism.

--------------------------------------------------
# ENGINE CONTEXT

Expose runtime capabilities.

Example

engine.hosted_services

engine.tasks

engine.scheduler

engine.async_runtime

Avoid exposing implementation classes.

--------------------------------------------------
# TESTS

Add comprehensive tests covering

HostedService lifecycle

TaskManager

CancellationToken

Scheduler execution

AsyncRuntime

Graceful shutdown

Failure rollback

Thread safety

Lifecycle ordering

Event publishing

Race condition regression tests

All existing tests must continue passing.

--------------------------------------------------
# DOCUMENTATION

Document Runtime Infrastructure.

Explain

Hosted Services

Task Manager

Scheduler

Cancellation

Async Runtime

Provide diagrams illustrating lifecycle integration.

--------------------------------------------------
# DO NOT CHANGE

Do NOT redesign

Kernel

Extension System

Dispatcher

Middleware

EngineContext

SDK

Public API

Architecture

Only add Runtime Infrastructure.

--------------------------------------------------
# ACCEPTANCE CRITERIA

✓ Engine can host long-running applications.

✓ Hosted Services integrate with lifecycle.

✓ Scheduler supports recurring jobs.

✓ TaskManager manages background execution.

✓ AsyncRuntime manages asyncio safely.

✓ CancellationToken supports cooperative cancellation.

✓ Runtime publishes lifecycle events.

✓ Graceful shutdown leaves no orphan threads.

✓ Existing applications remain compatible.

✓ All tests pass.

--------------------------------------------------
# OUTPUT

Provide

1. Runtime package tree

2. Lifecycle sequence diagram

3. Runtime architecture diagram

4. Public APIs introduced

5. Thread safety strategy

6. Failure recovery strategy

7. Test summary

Do not implement trading logic.

Do not implement Binance integration.

Do not implement UI frameworks.

Only build a generic Runtime Infrastructure suitable for any application.
```

---

## Mình còn đề xuất thêm một yêu cầu nhỏ vào prompt

Thêm mục này ngay trước **Acceptance Criteria**:

```text
# PERFORMANCE REQUIREMENTS

Runtime components should be lightweight.

Avoid unnecessary thread creation.

Reuse worker threads whenever possible.

Do not busy-wait.

Avoid polling when event-driven alternatives exist.

Startup overhead should remain minimal.

Memory footprint should stay low.

Design for applications expected to run continuously for weeks without restart.
```

Lý do là Sagittarius đang hướng tới **desktop app + trading bot + daemon**, tức là các ứng dụng có thể chạy liên tục hàng tuần hoặc hàng tháng. Nếu đưa yêu cầu về hiệu năng và độ ổn định vào ngay từ Phase 7, AI sẽ có xu hướng thiết kế `TaskManager`, `Scheduler` và `HostedServiceManager` bền vững hơn, thay vì chỉ làm cho đủ chức năng. Đây là thời điểm phù hợp nhất để đặt các tiêu chí đó, trước khi runtime trở thành nền tảng ổn định cho v1.0.
