> Applies to Sagittarius Engine v1.x

# Task Manager

## Runtime Component Relationships

Application -> TaskManager -> Thread Pool -> Worker Threads

## Overview

The `TaskManager` is the core background execution engine. It manages a Thread Pool designed to execute CPU-bound and IO-bound work without blocking the main application thread.

## Why

If an application handles a web request and needs to process a heavy calculation or send a slow email, doing so on the main thread will block other operations. The `TaskManager` provides a safe, managed way to offload fire-and-forget tasks to background threads.

## When to Use

Use the Task Manager for:
- One-off background tasks.
- CPU-heavy processing.
- Slow, blocking IO operations (if an async equivalent is unavailable).

## When NOT to Use

Do NOT use the Task Manager for:
- Continuous background loops (use [Hosted Services](hosted_services.md)).
- Tasks that must execute on a strict schedule (use the [Scheduler](scheduler.md)).

## Runtime Responsibilities

1. **Thread Pool Management**: Maintains a pool of reusable worker threads.
2. **Task Metadata**: Tracks executing tasks, their arguments, and execution times.
3. **Execution Routing**: Routes CPU-bound and IO-bound work to the appropriate background threads.
4. **Task Cleanup**: Automatically cleans up memory and metadata once a task completes.
5. **Cancellation**: Injects `CancellationToken` instances into tasks so they can be aborted during shutdown.

## Lifecycle

1. `spawn()`: A developer submits a function. The TaskManager wraps it in task metadata.
2. *Queued*: The task waits for an available worker thread.
3. *Running*: A worker thread picks up the task and executes it.
4. *Completed / Errored*: The task finishes. The TaskManager logs the result and performs Task Cleanup.

## Architecture

```mermaid
flowchart TB
    App[Application] -->|spawn(task)| TM[TaskManager]
    TM -->|Queue| P[Thread Pool]
    P -->|Assign| W1[Worker Thread 1]
    P -->|Assign| W2[Worker Thread 2]
    W1 -->|Execute| Task[Your Code]
    Task -->|Complete| TM
```

## Basic Example

```python
import time
from sagittarius_engine import App
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus

def send_welcome_email(username: str):
    print(f"Sending email to {username}...")
    time.sleep(0.1)
    print(f"Email sent to {username}.")

def main():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)
    app.boot()
    
    # Spawn a background task
    app.context.tasks.spawn(send_welcome_email, username="alice")
    
    time.sleep(0.2)
    app.stop()
```

## Advanced Example

```python
import time
from sagittarius_engine import App
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus

def heavy_calculation():
    print("Starting calculation...")
    for i in range(5):
        time.sleep(0.05)
    print("Calculation finished.")

def main():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)
    app.boot()
    
    app.context.tasks.spawn(heavy_calculation)
    
    time.sleep(0.1)
    app.stop()
```

## Best Practices

- Always accept a `CancellationToken` in your background tasks if they run for more than a few milliseconds (if the task manager supports injecting it).
- Avoid modifying global state from within tasks to prevent race conditions.

## Common Mistakes

- **Starting raw threads**: Using `threading.Thread(target=...)` bypasses the TaskManager. This means the engine cannot track the task, it will not receive a `CancellationToken`, and it may prevent graceful shutdown.

## Related Concepts

- [Concepts: Lifecycle](../concepts/lifecycle.md)

## Related Runtime Guides

- [Scheduler](scheduler.md)
- [Hosted Services](hosted_services.md)
- [Cancellation Token](cancellation_token.md)

## Related Tutorials

- *(No tutorials yet)*

## Related API Reference

- [TaskManager](../api/task_manager.md)

> [Found an issue? Edit this page on GitHub.](#)
