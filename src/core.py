from typing import Any

from src.application.event_bus_port import IEventBus
from src.application.command_port import ICommand
from src.application.query_port import IQuery
from src.application.module_port import IModule
from src.application.container_port import IContainer

class ModuleRegistrationError(Exception):
    pass

class BaseModule(IModule):
    def register(self, app: 'App') -> None:
        pass

    def boot(self, app: 'App') -> None:
        pass

class App:
    def __init__(self, container: IContainer, event_bus: IEventBus) -> None:
        self.container = container
        self.event_bus = event_bus
        self.modules: list[IModule] = []

    def use(self, module: IModule) -> None:
        if not isinstance(module, IModule):
            raise ModuleRegistrationError("Module must implement IModule")
        self.modules.append(module)
        module.register(self)

    def boot(self) -> None:
        for module in self.modules:
            module.boot(self)
        self.event_bus.emit('app.booted', self)

    def execute(self, command_class: type[ICommand], input_dto: Any = None) -> Any:
        command = self.container.resolve(command_class)
        return command.execute(input_dto)

    def query(self, query_class: type[IQuery], input_dto: Any = None) -> Any:
        query = self.container.resolve(query_class)
        return query.execute(input_dto)
