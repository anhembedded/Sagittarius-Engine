from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, Union, Optional
import inspect
import pkgutil
import importlib

T = TypeVar('T')

class ICommand(ABC):
    @abstractmethod
    def execute(self, input_dto: Any) -> Any:
        ...

class IQuery(ABC):
    @abstractmethod
    def execute(self, input_dto: Any) -> Any:
        ...

class IModule(ABC):
    @abstractmethod
    def register(self, app: 'App') -> None:
        ...

    @abstractmethod
    def boot(self, app: 'App') -> None:
        ...

class IContainer(ABC):
    @abstractmethod
    def bind(self, abstract: type, concrete: type) -> None:
        ...

    @abstractmethod
    def singleton(self, abstract: type, instance_or_factory: Union[Any, Callable]) -> None:
        ...

    @abstractmethod
    def resolve(self, abstract: type[T]) -> T:
        ...

class IEventBus(ABC):
    @abstractmethod
    def emit(self, event_name: str, data: Any = None) -> None:
        ...

    @abstractmethod
    def on(self, event_name: str, handler: Callable) -> None:
        ...

    @abstractmethod
    def off(self, event_name: str, handler: Callable) -> None:
        ...

class IMiddleware(ABC):
    @abstractmethod
    def process(self, cmd_or_query: Any, dto: Any, next_handler: Callable[[], Any]) -> Any:
        ...

class IConfig(ABC):
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        ...

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        ...

class ModuleRegistrationError(Exception):
    pass

class DependencyResolutionError(Exception):
    pass

class BaseModule(IModule):
    def register(self, app: 'App') -> None:
        pass

    def boot(self, app: 'App') -> None:
        pass

class MiddlewarePipeline:
    def __init__(self) -> None:
        self.middlewares: list[IMiddleware] = []

    def add(self, middleware: IMiddleware) -> None:
        self.middlewares.append(middleware)

    def execute(self, cmd_or_query: Any, dto: Any, final_handler: Callable[[], Any]) -> Any:
        def build_chain(index: int) -> Callable[[], Any]:
            if index < len(self.middlewares):
                middleware = self.middlewares[index]
                next_handler = build_chain(index + 1)
                return lambda: middleware.process(cmd_or_query, dto, next_handler)
            else:
                return final_handler

        chain = build_chain(0)
        return chain()

class ModuleAutoDiscovery:
    @staticmethod
    def discover(modules_package: str, app: 'App') -> None:
        try:
            package = importlib.import_module(modules_package)
        except ImportError:
            return

        if not hasattr(package, '__path__'):
            return

        for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
            if is_pkg:
                full_module_name = f"{modules_package}.{name}"
                sub_package = importlib.import_module(full_module_name)

                for _, obj in inspect.getmembers(sub_package, inspect.isclass):
                    if issubclass(obj, IModule) and obj is not IModule and obj is not BaseModule:
                        app.use(obj())


class App:
    def __init__(self, container: IContainer, event_bus: IEventBus) -> None:
        self.container = container
        self.event_bus = event_bus
        self.modules: list[IModule] = []
        self.pipeline = MiddlewarePipeline()

    def use(self, module: IModule) -> None:
        if not isinstance(module, IModule):
            raise ModuleRegistrationError("Module must implement IModule")
        self.modules.append(module)
        module.register(self)

    def use_middleware(self, middleware: IMiddleware) -> None:
        self.pipeline.add(middleware)

    def boot(self, auto_discover: Optional[str] = None) -> None:
        if auto_discover:
            ModuleAutoDiscovery.discover(auto_discover, self)
        for module in self.modules:
            module.boot(self)
        self.event_bus.emit('app.booted', self)

    def execute(self, command_class: type[ICommand], input_dto: Any = None) -> Any:
        command = self.container.resolve(command_class)
        def final() -> Any:
            return command.execute(input_dto)
        return self.pipeline.execute(command, input_dto, final)

    def query(self, query_class: type[IQuery], input_dto: Any = None) -> Any:
        query = self.container.resolve(query_class)
        def final() -> Any:
            return query.execute(input_dto)
        return self.pipeline.execute(query, input_dto, final)
