import asyncio
import time
from sagittarius_engine import App
from sagittarius_engine.runtime import IHostedService, CancellationToken


class MockWebSocketClient(IHostedService):
    """
    @brief Simulates a WebSocket client with auto-reconnect and heartbeat.
    """

    def __init__(self, app: App) -> None:
        self.app = app
        self.logger = app.context.logger
        self.token = CancellationToken()
        self._main_task = None

    def start(self, context) -> None:
        # Spawn the async connection loop on the AsyncRuntime
        self._main_task = self.app.context.tasks.spawn(
            self.connect_and_listen, name="WebSocketClient", token=self.token
        )
        self.logger.info("WebSocket Hosted Service started.")

    def stop(self, context) -> None:
        # Cancel the connection loop
        self.token.cancel()
        self.logger.info("WebSocket Hosted Service stopping...")
        if self._main_task and self._main_task.future:
            try:
                self._main_task.future.result(timeout=2.0)
            except Exception:
                pass
        self.logger.info("WebSocket Hosted Service stopped.")

    async def connect_and_listen(self, token: CancellationToken) -> None:
        backoff = 0.01
        while not token.is_cancelled():
            try:
                self.logger.info("[WebSocket] Attempting connection...")
                # Simulate network connection delay
                await asyncio.sleep(0.01)

                self.logger.info("[WebSocket] Connected! Starting heartbeat...")
                backoff = 0.01  # Reset backoff on success

                # Start heartbeat coroutine task on loop
                heartbeat = asyncio.create_task(self.heartbeat_loop(token))

                # Listen to incoming messages
                while not token.is_cancelled():
                    # Simulate periodic tick stream or tick packet receipt
                    await asyncio.sleep(0.05)
                    self.logger.info("[WebSocket] Received price tick update.")

                    # Simulate connection drop after some packets
                    self.logger.warning("[WebSocket] Connection dropped by peer!")
                    break

                heartbeat.cancel()
                try:
                    await heartbeat
                except asyncio.CancelledError:
                    pass

            except Exception as e:
                self.logger.error(f"[WebSocket] Connection error: {e}")

            if not token.is_cancelled():
                self.logger.info(
                    f"[WebSocket] Reconnecting in {backoff}s..."
                )
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 0.5)

    async def heartbeat_loop(self, token: CancellationToken) -> None:
        while not token.is_cancelled():
            try:
                await asyncio.sleep(0.03)
                self.logger.info("[WebSocket] Heartbeat PING sent.")
            except asyncio.CancelledError:
                break


def main():
    from sagittarius_engine.infrastructure.container.std_container import (
        StdLibContainer,
    )
    from sagittarius_engine.infrastructure.event_bus.memory_event_bus import (
        MemoryEventBus,
    )
    from sagittarius_engine.extensions.logger_module import LoggerExtension

    # 1. Initialize core container and event bus
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container=container, event_bus=event_bus)

    # 2. Add extensions
    app.use(LoggerExtension())

    # Create client
    client = MockWebSocketClient(app)
    app.context.hosted_services.register(client)

    app.boot()

    # Let connection run and drop/reconnect once
    time.sleep(0.2)

    # Shut down gracefully
    app.stop()


if __name__ == "__main__":
    main()
