from dataclasses import dataclass

from sagittarius_engine.domain.base_event import BaseEvent
from sagittarius_engine.extensions.cqrs.interfaces.commands import ICommand
from sagittarius_engine.extensions.cqrs.interfaces.queries import IQuery
from sagittarius_engine.infrastructure.config.dict_config import DictConfig
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from sagittarius_engine.kernel.app import App


# 1. Typed Domain Models & Events
class UserCreatedEvent(BaseEvent):
    def __init__(self, user_id: int, username: str) -> None:
        super().__init__()
        self.user_id = user_id
        self.username = username


@dataclass
class CreateUserDTO:
    user_id: int
    username: str


@dataclass
class GetUserQueryDTO:
    user_id: int


# 2. Typed Command & Query Handlers
class CreateUserCommandHandler(ICommand[CreateUserDTO, bool]):
    def execute(self, input_dto: CreateUserDTO) -> bool:
        return True if input_dto.user_id > 0 else False


class GetUserQueryHandler(IQuery[GetUserQueryDTO, str]):
    def execute(self, input_dto: GetUserQueryDTO) -> str:
        return f"User_{input_dto.user_id}"


def test_container_typing():
    container = StdLibContainer()
    container.singleton(DictConfig, DictConfig({"app.name": "Sagittarius"}))
    cfg = container.resolve(DictConfig)
    assert isinstance(cfg, DictConfig)
    assert cfg.get("app.name") == "Sagittarius"


def test_event_bus_class_based_typing():
    bus = MemoryEventBus()
    received_events: list[UserCreatedEvent] = []

    def on_user_created(event: UserCreatedEvent) -> None:
        received_events.append(event)

    bus.on(UserCreatedEvent, on_user_created)
    evt = UserCreatedEvent(user_id=42, username="Alice")
    bus.emit(evt)

    assert len(received_events) == 1
    assert received_events[0].user_id == 42
    assert received_events[0].username == "Alice"


def test_cqrs_strong_typing_dispatch():
    container = StdLibContainer()
    bus = MemoryEventBus()
    app = App(container, bus)

    app.container.bind(CreateUserCommandHandler, CreateUserCommandHandler)
    app.container.bind(GetUserQueryHandler, GetUserQueryHandler)

    cmd_res = app.dispatch(
        CreateUserCommandHandler, CreateUserDTO(user_id=1, username="Bob")
    )
    assert cmd_res is True

    query_res = app.dispatch(GetUserQueryHandler, GetUserQueryDTO(user_id=100))
    assert query_res == "User_100"


def test_typed_config():
    cfg = DictConfig({"port": 8080, "host": "127.0.0.1"})
    port: int = cfg.get("port", default=3000)
    assert port == 8080
    missing: int = cfg.get("missing_port", default=5000)
    assert missing == 5000
