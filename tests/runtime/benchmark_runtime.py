import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
import time

from sagittarius_engine import App
from sagittarius_engine.extensions.cqrs import ICommand
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from sagittarius_engine.interfaces import IMiddleware
from sagittarius_engine.runtime import IHostedService


class DummyHostedService(IHostedService):
    def start(self, context) -> None:
        pass

    def stop(self, context) -> None:
        pass


def run_boot_shutdown_benchmark():
    print("Running Benchmark: 100 App Boot/Shutdown Cycles...")
    start_time = time.perf_counter()

    for _ in range(100):
        app = App(StdLibContainer(), MemoryEventBus())
        app.boot()
        app.stop()

    end_time = time.perf_counter()
    total_duration = end_time - start_time
    avg_duration = total_duration / 100.0
    print(f"-> Total Time: {total_duration:.4f}s")
    print(f"-> Avg Time per Cycle: {avg_duration * 1000.0:.2f}ms\n")


def run_scheduler_load_benchmark():
    print("Running Benchmark: 1000 Scheduled Jobs under load...")
    app = App(StdLibContainer(), MemoryEventBus())
    app.boot()

    def dummy_job():
        pass

    start_time = time.perf_counter()

    for i in range(1000):
        app.context.scheduler.every(seconds=10.0 + i).do(dummy_job)

    end_time = time.perf_counter()
    app.stop()

    total_duration = end_time - start_time
    print(f"-> Time to add 1000 jobs: {total_duration * 1000.0:.2f}ms\n")


def run_hosted_services_benchmark():
    print("Running Benchmark: 100 Registered Hosted Services Lifecycle...")
    app = App(StdLibContainer(), MemoryEventBus())

    for _ in range(100):
        app.context.hosted_services.register(DummyHostedService())

    start_time = time.perf_counter()
    app.boot()
    app.stop()
    end_time = time.perf_counter()

    total_duration = end_time - start_time
    print(
        f"-> Boot/Shutdown latency for 100 hosted services: {total_duration * 1000.0:.2f}ms\n"
    )


def run_eventbus_latency_benchmark():
    print("Running Benchmark: Emit 10,000 Events with 10 Handlers...")
    bus = MemoryEventBus()

    # Register 10 dummy handlers
    counter = {"calls": 0}

    def handler(event_data):
        counter["calls"] += 1

    def make_handler():
        return lambda e: handler(e)

    for _ in range(10):
        bus.on("test.event", make_handler())

    start_time = time.perf_counter()

    for _ in range(10000):
        bus.emit("test.event", {"data": "test"})

    end_time = time.perf_counter()
    total_duration = end_time - start_time

    print(
        f"-> Time to emit 10,000 events (100,000 handler calls): {total_duration * 1000.0:.2f}ms"
    )
    print(f"-> Expected 100000 calls, got {counter['calls']}\n")


def run_middleware_overhead_benchmark():
    print("Running Benchmark: Dispatch Command through 10 Middlewares 10,000 times...")
    container = StdLibContainer()
    bus = MemoryEventBus()
    app = App(container, bus)

    class DummyMiddleware(IMiddleware):
        def process(self, cmd_or_query, data_transfer_obj, next_handler):
            # simulate a tiny bit of processing
            return next_handler()

    # Add 10 middlewares
    for _ in range(10):
        app.use_middleware(DummyMiddleware())

    class BenchmarkCommand(ICommand):
        def execute(self, data):
            return True

    container.bind(BenchmarkCommand, BenchmarkCommand)

    start_time = time.perf_counter()
    for _ in range(10000):
        app.dispatch(BenchmarkCommand, {})

    end_time = time.perf_counter()
    total_duration = end_time - start_time
    print(
        f"-> Time to dispatch 10,000 commands (each passing 10 middlewares): {total_duration * 1000.0:.2f}ms\n"
    )


def run_di_resolution_benchmark():
    print("Running Benchmark: Deep DI Graph Resolution (10,000 times)...")
    container = StdLibContainer()

    # Create a deep dependency graph
    class DepE:
        pass

    class DepD:
        def __init__(self, e: DepE):
            pass

    class DepC:
        def __init__(self, d: DepD):
            pass

    class DepB:
        def __init__(self, c: DepC):
            pass

    class DepA:
        def __init__(self, b: DepB, c: DepC, d: DepD, e: DepE):
            pass

    container.bind(DepE, DepE)
    container.bind(DepD, DepD)
    container.bind(DepC, DepC)
    container.bind(DepB, DepB)
    container.bind(DepA, DepA)

    start_time = time.perf_counter()
    for _ in range(10000):
        _ = container.resolve(DepA)
    end_time = time.perf_counter()

    total_duration = end_time - start_time
    print(
        f"-> Time to resolve 10,000 complex dependency graphs: {total_duration * 1000.0:.2f}ms\n"
    )


def main():
    logging.getLogger("App").setLevel(logging.ERROR)

    print("==================================================")
    print("           SAGITTARIUS RUNTIME BENCHMARKS         ")
    print("==================================================")

    run_boot_shutdown_benchmark()
    run_scheduler_load_benchmark()
    run_hosted_services_benchmark()
    run_eventbus_latency_benchmark()
    run_middleware_overhead_benchmark()
    run_di_resolution_benchmark()

    print("==================================================")


if __name__ == "__main__":
    main()
