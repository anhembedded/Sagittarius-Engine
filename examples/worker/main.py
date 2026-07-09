import time
import queue
from sagittarius_engine import App
from sagittarius_engine.runtime import IHostedService, CancellationToken


class QueueWorkerService(IHostedService):
    """
    @brief Processes jobs from a queue in the background.
    """

    def __init__(self, app: App) -> None:
        self.app = app
        self.logger = app.context.logger
        self.job_queue = queue.Queue()
        self.token = CancellationToken()
        self.task = None

    def start(self, context) -> None:
        # Spawn the background queue consumer loop
        self.task = self.app.context.tasks.spawn(
            self.consume_loop, name="QueueConsumer", token=self.token
        )
        self.logger.info("Queue worker started.")

    def stop(self, context) -> None:
        # Signal cooperative cancellation
        self.token.cancel()
        self.logger.info("Cancellation signalled to queue worker.")

        # Wait for the consumer thread to finish processing
        if self.task and self.task.future:
            try:
                self.task.future.result(timeout=2.0)
            except Exception:
                pass
        self.logger.info("Queue worker stopped.")

    def add_job(self, data: str) -> None:
        self.job_queue.put(data)
        self.logger.info(f"[Producer] Queued job: '{data}'")

    def consume_loop(self, token: CancellationToken) -> None:
        while not token.is_cancelled():
            try:
                # Wait with timeout so we check cancellation regularly
                job = self.job_queue.get(timeout=0.02)
                self.logger.info(f"[Consumer] Processing job: '{job}'...")
                time.sleep(0.05)  # Simulate work
                self.logger.info(f"[Consumer] Completed job: '{job}'")
                self.job_queue.task_done()
            except queue.Empty:
                continue


def main():
    from sagittarius_engine.infrastructure.container.std_container import (
        StdLibContainer,
    )
    from sagittarius_engine.infrastructure.event_bus.memory_event_bus import (
        MemoryEventBus,
    )
    from sagittarius_engine.extensions.logger_module import LoggerModule

    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    # Use logging
    app.use(LoggerModule())

    # Create worker
    worker = QueueWorkerService(app)
    app.context.hosted_services.register(worker)

    app.boot()

    # Produce jobs
    worker.add_job("Import Transactions")
    worker.add_job("Generate Reports")
    worker.add_job("Send Email Notifications")

    # Let the worker run briefly
    time.sleep(0.2)

    # Shut down the app gracefully
    app.stop()


if __name__ == "__main__":
    main()
