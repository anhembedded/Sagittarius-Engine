import time




def test_thread_pool_event_bus_execution(thread_pool_bus_factory):
    bus = thread_pool_bus_factory(max_workers=2)
    results = []

    def handler1(data):
        time.sleep(0.1)
        results.append(f"handler1: {data}")

    def handler2(data):
        results.append(f"handler2: {data}")

    bus.on("test.event", handler1)
    bus.on("test.event", handler2)

    bus.emit("test.event", "payload")

    # Wait for the async tasks to complete
    time.sleep(0.2)

    assert "handler1: payload" in results
    assert "handler2: payload" in results
    assert len(results) == 2


def test_thread_pool_event_bus_exception_handling(thread_pool_bus_factory):
    bus = thread_pool_bus_factory(max_workers=2)
    results = []

    def failing_handler(data):
        raise ValueError("Intentional failure")

    def successful_handler(data):
        results.append(f"success: {data}")

    bus.on("test.event", failing_handler)
    bus.on("test.event", successful_handler)

    # This should not raise an exception
    bus.emit("test.event", "payload")

    # Wait for the async tasks to complete
    time.sleep(0.1)

    assert "success: payload" in results
    assert len(results) == 1


def test_thread_pool_event_bus_on_off(thread_pool_bus_factory):
    bus = thread_pool_bus_factory()
    results = []

    def handler(data):
        results.append(data)

    bus.on("test.event", handler)
    bus.emit("test.event", "data1")

    time.sleep(0.1)
    assert results == ["data1"]

    bus.off("test.event", handler)
    bus.emit("test.event", "data2")
    # Shouldn't receive data2
    time.sleep(0.1)
    assert results == ["data1"]
