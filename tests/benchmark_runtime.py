import time
import logging
from sagittarius_engine import App
from sagittarius_engine.runtime import IHostedService
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus


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

    # Define simple mock work
    def dummy_job():
        pass

    start_time = time.perf_counter()

    # Add 1000 scheduler jobs
    for i in range(1000):
        app.context.scheduler.every(seconds=10.0 + i).do(dummy_job)

    end_time = time.perf_counter()
    app.stop()

    total_duration = end_time - start_time
    print(f"-> Time to add 1000 jobs: {total_duration * 1000.0:.2f}ms\n")


def run_hosted_services_benchmark():
    print("Running Benchmark: 100 Registered Hosted Services Lifecycle...")
    app = App(StdLibContainer(), MemoryEventBus())

    # Register 100 hosted services
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


def main():
    # Disable logs during benchmark
    logging.getLogger("App").setLevel(logging.ERROR)

    print("==================================================")
    print("           SAGITTARIUS RUNTIME BENCHMARKS         ")
    print("==================================================")

    run_boot_shutdown_benchmark()
    run_scheduler_load_benchmark()
    run_hosted_services_benchmark()

    print("==================================================")


if __name__ == "__main__":
    main()
