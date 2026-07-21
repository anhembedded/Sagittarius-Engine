from sagittarius_engine import App

from sagittarius_engine.infrastructure.event_bus import InMemoryEventBus
from sagittarius_engine.infrastructure.container import StdLibContainer

container = StdLibContainer()
event_bus = InMemoryEventBus()

app = App(container, event_bus)
app.dispatch()

app.boot()


app.stop()