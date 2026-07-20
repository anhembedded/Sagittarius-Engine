from sagittarius_engine.infrastructure.container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus import MemoryEventBus
from sagittarius_engine.kernel import App


def main():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    app.boot()
    print("Minimal App 'my_bot' booted successfully by Developer!")


if __name__ == "__main__":
    main()
