import asyncio
import warnings

import pytest

from sagittarius_engine.infrastructure.event_bus.asyncio_event_bus import (
    AsyncioEventBus,
)


@pytest.mark.asyncio
async def test_asyncio_event_bus_mixed_handlers():
    bus = AsyncioEventBus()
    results = []

    async def async_handler(data):
        await asyncio.sleep(0.01)
        results.append(f"async: {data}")

    def sync_handler(data):
        results.append(f"sync: {data}")

    bus.on("test.event", async_handler)
    bus.on("test.event", sync_handler)

    await bus.emit("test.event", "payload")

    # Ensure both handlers executed successfully sequentially
    assert results == ["async: payload", "sync: payload"]


@pytest.mark.asyncio
async def test_asyncio_event_bus_avoids_deprecated_coroutine_check():
    bus = AsyncioEventBus()
    results = []

    async def async_handler(data):
        results.append(f"async: {data}")

    bus.on("test.event", async_handler)

    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        await bus.emit("test.event", "payload")

    assert results == ["async: payload"]


@pytest.mark.asyncio
async def test_asyncio_event_bus_exception_handling():
    bus = AsyncioEventBus()
    results = []

    async def failing_async_handler(data):
        raise ValueError("Async fail")

    def failing_sync_handler(data):
        raise ValueError("Sync fail")

    def successful_handler(data):
        results.append(f"success: {data}")

    bus.on("test.event", failing_async_handler)
    bus.on("test.event", failing_sync_handler)
    bus.on("test.event", successful_handler)

    # Should not raise exception
    await bus.emit("test.event", "payload")

    # The successful handler should still run since exceptions are caught
    assert results == ["success: payload"]


@pytest.mark.asyncio
async def test_asyncio_event_bus_on_off():
    bus = AsyncioEventBus()
    results = []

    async def handler(data):
        results.append(data)

    bus.on("test.event", handler)
    await bus.emit("test.event", "data1")
    assert results == ["data1"]

    bus.off("test.event", handler)
    await bus.emit("test.event", "data2")
    assert results == ["data1"]
