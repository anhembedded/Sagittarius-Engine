import time
from sagittarius_engine import App, IExtension, ExtensionDescriptor


class MetricsPlugin(IExtension):
    def __init__(self) -> None:
        self._desc = ExtensionDescriptor(name="MetricsPlugin", priority=10)
        self.initialized = False

    @property
    def descriptor(self) -> ExtensionDescriptor:
        return self._desc

    def register(self, context) -> None:
        self.initialized = True
        context.logger.info("[MetricsPlugin] Registered.")

    def boot(self, context) -> None:
        context.logger.info("[MetricsPlugin] Started.")

    def shutdown(self, context) -> None:
        context.logger.info("[MetricsPlugin] Stopped.")

    def dispose(self, context) -> None:
        context.logger.info("[MetricsPlugin] Disposed.")


class TradingPlugin(IExtension):
    def __init__(self) -> None:
        self._desc = ExtensionDescriptor(
            name="TradingPlugin", dependencies=["MetricsPlugin"], priority=5
        )
        self.initialized = False

    @property
    def descriptor(self) -> ExtensionDescriptor:
        return self._desc

    def register(self, context) -> None:
        self.initialized = True
        context.logger.info("[TradingPlugin] Registered.")

    def boot(self, context) -> None:
        context.logger.info("[TradingPlugin] Started.")

    def shutdown(self, context) -> None:
        context.logger.info("[TradingPlugin] Stopped.")

    def dispose(self, context) -> None:
        context.logger.info("[TradingPlugin] Disposed.")


class DashboardPlugin(IExtension):
    def __init__(self) -> None:
        self._desc = ExtensionDescriptor(
            name="DashboardPlugin", dependencies=["TradingPlugin"], priority=0
        )
        self.initialized = False

    @property
    def descriptor(self) -> ExtensionDescriptor:
        return self._desc

    def register(self, context) -> None:
        self.initialized = True
        context.logger.info("[DashboardPlugin] Registered.")

    def boot(self, context) -> None:
        context.logger.info("[DashboardPlugin] Started.")

    def shutdown(self, context) -> None:
        context.logger.info("[DashboardPlugin] Stopped.")

    def dispose(self, context) -> None:
        context.logger.info("[DashboardPlugin] Disposed.")


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

    # Register plugins in REVERSE dependency order: Dashboard -> Trading -> Metrics
    app.use(DashboardPlugin())
    app.use(TradingPlugin())
    app.use(MetricsPlugin())

    # Boot the application
    app.boot()

    # Let the application run briefly
    time.sleep(0.05)

    # Stop the application
    app.stop()


if __name__ == "__main__":
    main()
