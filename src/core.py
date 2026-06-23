import inspect
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Type, TypeVar, Union

T = TypeVar('T')

class DependencyResolutionError(Exception):
    pass

class ModuleRegistrationError(Exception):
    pass

class IEventBus(ABC):
    @abstractmethod
    def emit(self, event_name: str, data: Any = None) -> None:
        pass

    @abstractmethod
    def on(self, event_name: str, handler: Callable) -> None:
        pass

    @abstractmethod
    def off(self, event_name: str, handler: Callable) -> None:
        pass

class ICommand(ABC):
    @abstractmethod
    def execute(self, input_dto: Any) -> Any:
        pass

class IQuery(ABC):
    @abstractmethod
    def execute(self, input_dto: Any) -> Any:
        pass

class IModule(ABC):
    @abstractmethod
    def register(self, app: 'App') -> None:
        pass

    @abstractmethod
    def boot(self, app: 'App') -> None:
        pass

class Container:
    def __init__(self):
        self._bindings: Dict[Type, Type] = {}
        self._instances: Dict[Type, Any] = {}
        self._factories: Dict[Type, Callable] = {}

    def bind(self, abstract: Type, concrete: Type) -> None:
        self._bindings[abstract] = concrete

    def singleton(self, abstract: Type, instance_or_factory: Union[Any, Callable]) -> None:
        if callable(instance_or_factory) and not isinstance(instance_or_factory, type):
            self._factories[abstract] = instance_or_factory
        else:
            self._instances[abstract] = instance_or_factory

    def resolve(self, abstract: Type[T]) -> T:
        if abstract in self._instances:
            return self._instances[abstract]

        if abstract in self._factories:
            instance = self._factories[abstract](self)
            self._instances[abstract] = instance
            return instance

        concrete = self._bindings.get(abstract, abstract)

        if not inspect.isclass(concrete):
            raise DependencyResolutionError(f"Cannot resolve {abstract}")

        if getattr(concrete, "__abstractmethods__", None):
            raise DependencyResolutionError(f"Cannot instantiate abstract class {concrete}")

        if getattr(concrete, "__init__", None) is object.__init__:
            return concrete()

        try:
            signature = inspect.signature(concrete.__init__)
        except ValueError:
            return concrete()

        dependencies = {}
        for name, param in signature.parameters.items():
            if name == 'self' or name == 'args' or name == 'kwargs':
                continue
            if param.annotation == inspect.Parameter.empty:
                raise DependencyResolutionError(f"Missing type hint for parameter '{name}' in {concrete.__name__}")
            try:
                dependencies[name] = self.resolve(param.annotation)
            except Exception as e:
                raise DependencyResolutionError(f"Failed to resolve '{name}' for {concrete.__name__}: {str(e)}")

        instance = concrete(**dependencies)
        return instance

class EventBus(IEventBus):
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}

    def emit(self, event_name: str, data: Any = None) -> None:
        for handler in self._handlers.get(event_name, []):
            handler(data)

    def on(self, event_name: str, handler: Callable) -> None:
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        if handler not in self._handlers[event_name]:
            self._handlers[event_name].append(handler)

    def off(self, event_name: str, handler: Callable) -> None:
        if event_name in self._handlers and handler in self._handlers[event_name]:
            self._handlers[event_name].remove(handler)

class BaseModule(IModule):
    def register(self, app: 'App') -> None:
        pass

    def boot(self, app: 'App') -> None:
        pass

class App:
    def __init__(self):
        self.container = Container()
        self.event_bus = EventBus()
        self.modules: List[IModule] = []

        self.container.singleton(IEventBus, self.event_bus)
        self.container.singleton(Container, self.container)
        self.container.singleton('App', self)

    def use(self, module: IModule) -> None:
        if not isinstance(module, IModule):
            raise ModuleRegistrationError("Module must implement IModule")
        self.modules.append(module)
        module.register(self)

    def boot(self) -> None:
        for module in self.modules:
            module.boot(self)
        self.event_bus.emit('app.booted', self)

    def execute(self, command_class: Type[ICommand], input_dto: Any) -> Any:
        command = self.container.resolve(command_class)
        return command.execute(input_dto)

    def query(self, query_class: Type[IQuery], input_dto: Any) -> Any:
        query = self.container.resolve(query_class)
        return query.execute(input_dto)
