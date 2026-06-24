import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.app_kernel import App
from src.infra.std_container import StdLibContainer
from src.infra.memory_event_bus import MemoryEventBus
from src.interfaces import IEventBus

from example.multi_module.modules.user_module import UserModule
from example.multi_module.modules.notification_module import NotificationModule
from example.multi_module.application.create_user_command import CreateUserCommand, CreateUserDto

def main():
    print("--- Booting Application ---")
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    # Core bindings
    container.singleton(IEventBus, event_bus)

    # Register modules
    app.use(UserModule())
    app.use(NotificationModule())
    app.boot()

    print("\n--- Executing CreateUserCommand ---")
    dto = CreateUserDto(username="jules", email="jules@example.com")
    app.execute(CreateUserCommand, dto)

if __name__ == "__main__":
    main()
