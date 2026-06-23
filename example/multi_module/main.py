import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core import App, IEventBus
from src.infra.std_container import StdLibContainer
from src.infra.memory_event_bus import MemoryEventBus
from src.modules.logger_module import LoggerModule
from example.multi_module.modules.user_module import UserModule
from example.multi_module.modules.order_module import OrderModule
from example.multi_module.application.create_user_command import CreateUserCommand

def main():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    container.singleton(IEventBus, event_bus)

    app.use(LoggerModule())
    app.use(UserModule())
    app.use(OrderModule())
    app.boot()

    print("\n--- Testing Module Communication ---")
    app.execute(CreateUserCommand, {"name": "Alice"})

if __name__ == "__main__":
    main()
