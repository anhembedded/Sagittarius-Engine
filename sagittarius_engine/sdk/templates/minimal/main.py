from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from sagittarius_engine.kernel import App


def main():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    app.boot()
    print("Minimal App '{{project_name}}' booted successfully by {{author}}!")


if __name__ == "__main__":
    main()
