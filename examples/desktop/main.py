import time
from sagittarius_engine import App


class MockDesktopWindow:
    """
    @brief Simulates a general event-driven Desktop Window (such as PySide6/PyQt6/Tkinter).
    """

    def __init__(self, app: App) -> None:
        self.app = app
        self.logger = app.context.logger
        self.status_text = "Idle"

        # Register UI listener to engine event bus
        self.app.event_bus.on("ui.update_status", self.on_status_updated)

    def on_status_updated(self, event) -> None:
        self.status_text = event.text
        self.logger.info(f"[UI Thread] UI Label updated: {self.status_text}")

    def simulate_button_click(self) -> None:
        self.logger.info("[UI Thread] Button clicked! Spawning background work...")
        # Dispatch background work to the engine TaskManager
        self.app.context.tasks.spawn(self.perform_heavy_calc, name="HeavyCalc")

    def perform_heavy_calc(self) -> None:
        self.logger.info("[Worker Thread] Starting heavy calculations...")
        time.sleep(0.05)  # Simulated computation
        self.logger.info("[Worker Thread] Calculations finished. Notifying UI...")

        class UIEvent:
            def __init__(self, text: str) -> None:
                self.text = text

        self.app.event_bus.emit("ui.update_status", UIEvent("Task Complete!"))


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

    # Boot engine before UI launches
    app.boot()

    # Create UI
    window = MockDesktopWindow(app)

    # Simulate clicks and events
    window.simulate_button_click()

    # Give worker thread time to process and update UI
    time.sleep(0.1)

    # Shutdown
    app.stop()


if __name__ == "__main__":
    main()
