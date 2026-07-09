---
type: design_doc
tags: [sagittarius, event-bus, core]
language: python
---

# Event Bus Module

## Overview

The `event_bus` module provides implementations of the `IEventBus` and `IAsyncEventBus` interfaces, enabling decoupled communication between system components using the Publish/Subscribe pattern. It is the heart of the event-driven architecture in the Sagittarius Framework.

Available implementations:

- **MemoryEventBus** – synchronous, in‑memory, thread‑safe bus.
- **ThreadPoolEventBus** – executes handlers in a thread pool.
- **AsyncioEventBus** – runs handlers on an asyncio event loop.
- **ResilientEventBus** – decorator that adds retry logic and a Dead Letter Queue (DLQ).
- **IPCQueueEventBus** – inter‑process bus using `multiprocessing.Queue`.
- **IPCBroker** – helper that broadcasts events from a publish queue to multiple subscriber queues.

## Problem Statement

In a Clean Architecture, modules must communicate without tight coupling. Direct calls create hard dependencies that hinder testing and evolution. Moreover, different applications require different event processing strategies:

- Simple apps: synchronous, in‑process execution.
- I/O‑heavy apps: parallel execution to avoid blocking.
- Real‑time apps: asynchronous, non‑blocking handling.
- Distributed apps: inter‑process communication.

The Event Bus module solves these by offering multiple implementations behind the same interface, allowing developers to swap the bus without changing business logic.

## Proposed Solution

Define `IEventBus` (and `IAsyncEventBus`) as the common contract. Each implementation addresses a specific need:

| Implementation | Mechanism | Use when |
|----------------|-----------|----------|
| `MemoryEventBus` | Synchronous, thread‑safe | Simple applications, testing |
| `ThreadPoolEventBus` | Thread pool | Parallel I/O processing |
| `AsyncioEventBus` | asyncio | Async applications |
| `ResilientEventBus` | Retry + DLQ | High‑reliability requirements |
| `IPCQueueEventBus` | multiprocessing.Queue | Multiple processes |

All implementations are interchangeable via Dependency Injection.

## Core API / Interface

### `IEventBus` (src/interfaces/i_event_bus.py)

```python
class IEventBus(ABC):
    @abstractmethod
    def emit(self, event_name: str, data: Any = None) -> None: ...
    @abstractmethod
    def on(self, event_name: str, handler: Callable) -> None: ...
    @abstractmethod
    def off(self, event_name: str, handler: Callable) -> None: ...
```

### `IAsyncEventBus` (src/interfaces/i_async_event_bus.py)

```python
class IAsyncEventBus(Protocol):
    async def emit(self, event_name: str, data: Any = None) -> None: ...
    def on(self, event_name: str, handler: Callable) -> None: ...
    def off(self, event_name: str, handler: Callable) -> None: ...
```

### `MemoryEventBus`

- `class MemoryEventBus(logger: ILogger | None = None)`
- `emit(event_name: str, data: Any = None) -> None`
- `on(event_name: str, handler: Callable) -> None`
- `off(event_name: str, handler: Callable) -> None`
- Thread‑safe: uses `threading.Lock`; snapshots handlers before iterating to avoid deadlocks.

### `ThreadPoolEventBus`

- `class ThreadPoolEventBus(max_workers: int = 4, logger: ILogger | None = None)`
- `emit(event_name: str, data: Any = None) -> None` – submits handlers to `ThreadPoolExecutor`
- `on(event_name: str, handler: Callable) -> None`
- `off(event_name: str, handler: Callable) -> None`
- `shutdown(wait: bool = True) -> None` – shuts down the underlying executor

### `AsyncioEventBus`

- `class AsyncioEventBus(logger: ILogger | None = None)`
- `async emit(event_name: str, data: Any = None) -> None` – awaits handlers sequentially; supports both sync and async handlers
- `on(event_name: str, handler: Callable) -> None`
- `off(event_name: str, handler: Callable) -> None`

### `ResilientEventBus`

- `class ResilientEventBus(inner_bus: IEventBus, max_retries: int = 3, logger: ILogger | None = None)`
- `emit(event_name: str, data: Any = None) -> None` – retries failing handlers up to `max_retries` times
- `get_dlq() -> list[tuple[str, Any, Callable, Exception]]` – returns failed events
- `reprocess() -> None` – attempts to re‑process events currently in the DLQ

### `IPCQueueEventBus`

- `class IPCQueueEventBus(subscriber_queue: Queue | None = None, publish_queue: Queue | None = None, logger: ILogger | None = None)`
- `emit(event_name: str, data: Any = None) -> None` – puts the event into the shared publish queue
- `on(event_name: str, handler: Callable) -> None`
- `off(event_name: str, handler: Callable) -> None`
- `start() -> None` – starts the listener daemon thread that reads from `subscriber_queue`
- `stop() -> None` – stops the listener thread gracefully

### `IPCBroker`

- `class IPCBroker(publish_queue: Queue, logger: ILogger | None = None)`
- `add_subscriber(sub_queue: Queue) -> None`
- `remove_subscriber(sub_queue: Queue) -> None`
- `start() -> None` – starts a daemon thread that broadcasts messages from `publish_queue` to all subscriber queues
- `stop() -> None` – stops the broker thread

## Dependencies

- **Internal**: `src.interfaces.IEventBus`, `src.interfaces.IAsyncEventBus`, `src.interfaces.ILogger`
- **External**: `threading`, `asyncio`, `concurrent.futures`, `multiprocessing.queues.Queue`, `queue` (standard library)

## How to Use / Examples

### 1. MemoryEventBus

```python
from sagittarius_engine.infrastructure.event_bus import MemoryEventBus

bus = MemoryEventBus()
bus.on("user.created", lambda user: print(f"New user: {user['name']}"))
bus.emit("user.created", {"name": "Alice"})
```

### 2. ThreadPoolEventBus

```python
from sagittarius_engine.infrastructure.event_bus import ThreadPoolEventBus
import time

def slow_handler(data):
    time.sleep(2)
    print(f"Processed: {data}")

bus = ThreadPoolEventBus(max_workers=8)
bus.on("data.process", slow_handler)
bus.emit("data.process", {"id": 1})
bus.shutdown()
```

### 3. AsyncioEventBus

```python
import asyncio
from sagittarius_engine.infrastructure.event_bus import AsyncioEventBus

async def main():
    bus = AsyncioEventBus()
    bus.on("tick", lambda price: print(f"Price: {price}"))
    await bus.emit("tick", 100.5)

asyncio.run(main())
```

### 4. ResilientEventBus

```python
from sagittarius_engine.infrastructure.event_bus import MemoryEventBus, ResilientEventBus

base_bus = MemoryEventBus()
safe_bus = ResilientEventBus(base_bus, max_retries=3)

def handler(data):
    raise Exception("Network error")

safe_bus.on("api.call", handler)
safe_bus.emit("api.call", {"url": "..."})
print(safe_bus.get_dlq())  # contains failed events
```

### 5. IPCQueueEventBus (cross‑process)

```python
import multiprocessing
from sagittarius_engine.infrastructure.event_bus import IPCBroker, IPCQueueEventBus

def child_process(sub_queue, pub_queue):
    bus = IPCQueueEventBus(sub_queue, pub_queue)
    bus.on("task", lambda d: print(f"Child received: {d}"))
    bus.start()
    bus.emit("result", {"ok": True})
    bus.stop()

if __name__ == "__main__":
    manager = multiprocessing.Manager()
    pub_queue = manager.Queue()
    sub_queue = manager.Queue()

    broker = IPCBroker(pub_queue)
    broker.add_subscriber(sub_queue)
    broker.start()

    p = multiprocessing.Process(target=child_process, args=(sub_queue, pub_queue))
    p.start()
    p.join()

    broker.stop()
```

## Implementation Notes

- **Thread‑safety**: All buses use `threading.Lock` to protect handler lists. A snapshot of handlers is taken inside the lock before iteration, preventing deadlocks if a handler calls `on`/`off`.
- **Error handling**: Exceptions raised by handlers are caught and logged via `ILogger` (if available); the bus never crashes.
- **AsyncioEventBus**: Supports both sync and async handlers; executes them sequentially to reduce complexity. `CancelledError` is handled separately.
- **IPCQueueEventBus**: Requires an `IPCBroker` for broadcasting events to multiple processes. Uses sentinel messages (`_STOP_`) for graceful shutdown of listener threads.
- **ResilientEventBus**: Stores a private handler list to manage retries. The DLQ holds tuples of `(event_name, data, handler, exception)`. `reprocess()` tries to re‑execute DLQ entries and returns them to the queue if they still fail.

## Related Documents

- [Container Design Doc](container.md)
- [Middleware Design Doc](middleware.md)
- [IPC and Process Management](ipc.md)


