---
type: design_doc
tags: [sagittarius, eventbus]
language: python
---

# EventBus

## Overview
The `EventBus` provides a publish-subscribe (Pub/Sub) mechanism allowing different parts of the application to communicate in a loosely coupled manner. By defining domains of events and decoupling producers from consumers, it forms a critical piece of the framework's Event-Driven Architecture.

## Problem Statement
In large, decoupled systems, calling services or commands directly creates tight coupling, making the system difficult to modify and test. An event-driven architecture solves this by emitting events (e.g., `user.created`) that unknown observers (handlers) can listen to and act upon (e.g., sending an email, logging) without modifying the main execution flow.

## Proposed Solution
Sagittarius defines synchronous (`IEventBus`) and asynchronous (`IAsyncEventBus`) interfaces for event publishing and subscription. It provides multiple implementations tailored to different execution environments:
- **`MemoryEventBus`**: Synchronous, in-memory execution in the same thread. Thread-safe handler registry using `threading.Lock`.
- **`ThreadPoolEventBus`**: Executes handlers concurrently using Python's `ThreadPoolExecutor`. Best for CPU-bound or blocking I/O background tasks.
- **`AsyncioEventBus`**: Native asynchronous execution using Python's `asyncio`. Awaits coroutines sequentially inside the event loop.
- **`ResilientEventBus`**: A decorator pattern bus that adds retry mechanisms and a Dead Letter Queue (DLQ) for fault-tolerant event processing.

## Core API / Interface

### `interface IEventBus` / `IAsyncEventBus`
Abstract base class representing the Event Bus port.

- `def emit(self, event_name: str, data: Any=None) -> None` (or `async def emit` for `IAsyncEventBus`): Publishes an event and data payload.
- `def on(self, event_name: str, handler: Callable) -> None`: Subscribes a handler function.
- `def off(self, event_name: str, handler: Callable) -> None`: Unsubscribes a handler function.

### Implementations

#### `class MemoryEventBus(IEventBus)`
- `def __init__(self, logger: Optional[ILogger] = None) -> None`

#### `class ThreadPoolEventBus(IEventBus)`
- `def __init__(self, max_workers: int = 4, logger: Optional[ILogger] = None) -> None`
- `def shutdown(self, wait: bool = True) -> None`: Shuts down the thread pool executor.

#### `class AsyncioEventBus(IAsyncEventBus)`
- Supports mixed sync/async handler registrations.

#### `class ResilientEventBus(IEventBus)`
- `def __init__(self, inner_bus: IEventBus, max_retries: int = 3, logger: Optional[ILogger] = None) -> None`
- `def get_dlq(self) -> List[Tuple[str, Any, Callable, Exception]]`: Retrieves the Dead Letter Queue.
- `def reprocess(self) -> None`: Attempts to reprocess all events currently in the DLQ.

## Dependencies
- Internal: `ILogger`
- External: Standard libraries (`threading`, `concurrent.futures`, `asyncio`)

## How to Use / Examples

```python
from src.infra.memory_event_bus import MemoryEventBus
from src.infra.resilient_event_bus import ResilientEventBus
from src.infra.std_logger import StdLogger

logger = StdLogger()

# Basic Memory Event Bus
bus = MemoryEventBus(logger=logger)

# Handler function
def send_email(data):
    print(f"Sending email to {data['email']}")

# Subscription
bus.on('user.registered', send_email)

# Emit event
bus.emit('user.registered', {'email': 'test@example.com'})

# Using Resilient Decorator
safe_bus = ResilientEventBus(inner_bus=bus, max_retries=3)
safe_bus.emit('user.registered', {'email': 'fail@example.com'})

# Reprocess failed events
safe_bus.reprocess()
```

## Implementation Notes
- **Thread Safety**: Operations modifying the handler registry (`on`, `off`, `emit` snapshotting) are protected via `threading.Lock` across most implementations.
- **Error Handling**: Exception raised in handlers are caught and logged (via injected `ILogger`) to prevent breaking the event bus loop, ensuring other handlers still fire. `ThreadPoolEventBus` handles exceptions via `add_done_callback`.
- **Resilient Bus**: The `ResilientEventBus` acts as a decorator. Failed handlers are appended to a DLQ containing `(event_name, data, handler, exception)` which can be accessed for manual review or reprocessing.

## Related Documents
- `app_kernel.md`
- `base_event.md`
