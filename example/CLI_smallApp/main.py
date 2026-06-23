import sys
from pathlib import Path

# Add project root to path so we can import src
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from src.core import App
from src.application.container_port import IContainer
from src.application.event_bus_port import IEventBus
from src.infra.stdlib_container_infra import Container
from src.infra.memory_event_bus_infra import EventBus
from example.CLI_smallApp.modules.user_module import UserModule
from example.CLI_smallApp.adapters.cli import UserCLI

def main() -> None:
    print("Initializing Infrastructure...")
    container = Container()
    event_bus = EventBus()

    print("Registering Core Ports to Container in Composition Root...")
    container.singleton(IContainer, container)
    container.singleton(IEventBus, event_bus)

    print("Initializing Application...")
    app = App(container=container, event_bus=event_bus)
    container.singleton(App, app)

    print("Registering Modules...")
    app.use(UserModule())

    print("Booting Application...")
    app.boot()

    print("Starting CLI Adapter...")
    cli = UserCLI(app)
    cli.cmdloop()

if __name__ == "__main__":
    main()
