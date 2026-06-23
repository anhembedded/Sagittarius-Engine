import sys
import os

# Add root directory to path to allow absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.infra.std_container import StdLibContainer
from src.infra.memory_event_bus import MemoryEventBus
from src.core import App, IContainer, IEventBus
from src.middleware.logging_middleware import LoggingMiddleware
from example.CLI_smallApp.adapters.cli import run_cli

def main():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    # Register core ports
    container.singleton(IContainer, container)
    container.singleton(IEventBus, event_bus)

    # Add optional middleware
    app.use_middleware(LoggingMiddleware(container))

    # Auto-discover modules in the current package structure
    app.boot(auto_discover="example.CLI_smallApp.modules")

    # Run CLI loop or single command
    run_cli(app)

if __name__ == "__main__":
    main()
