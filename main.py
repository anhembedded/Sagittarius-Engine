import json
import os
from typing import Any

from sagittarius_engine.kernel import App
from sagittarius_engine.base import BaseModule
from sagittarius_engine.interfaces import ICommand, IQuery, IEventBus, IContainer, IConfig
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from sagittarius_engine.infrastructure.config.dict_config import DictConfig
from sagittarius_engine.extensions.logger_module import LoggerModule
from sagittarius_engine.middleware.logging_middleware import LoggingMiddleware

# ========== DOMAIN ==========
class User:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

# ========== INFRASTRUCTURE ==========
class FakeUserRepository:
    def __init__(self):
        self.users: list[User] = []
    def add(self, user: User): self.users.append(user)
    def all(self) -> list[User]: return self.users

# ========== MODULE ==========
class UserModule(BaseModule):
    def register(self, app: App):
        # Bind repo as singleton
        app.container.singleton(FakeUserRepository, FakeUserRepository())
        # Bind command
        app.container.bind(CreateUserCommand, CreateUserCommand)
        app.container.bind(ListUsersQuery, ListUsersQuery)

    def boot(self, app: App):
        app.event_bus.on('user.created', self.on_user_created)

    def on_user_created(self, user: User):
        print(f"[EVENT] User created: {user.name}")

# ========== COMMAND ==========
class CreateUserCommand(ICommand):
    def __init__(self, repo: FakeUserRepository, event_bus: IEventBus):
        self.repo = repo
        self.event_bus = event_bus

    # pyrefly: ignore [bad-override]
    def execute(self, input_dto: dict) -> User:
        user = User(id=input_dto['id'], name=input_dto['name'])
        self.repo.add(user)
        self.event_bus.emit('user.created', user)
        return user

# ========== QUERY ==========
class ListUsersQuery(IQuery):
    def __init__(self, repo: FakeUserRepository):
        self.repo = repo

    def execute(self, input_dto: Any = None) -> list[User]:
        return self.repo.all()

# ========== MAIN ==========
if __name__ == "__main__":
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    container.singleton(IContainer, container)
    container.singleton(IEventBus, event_bus)

    # Load configuration
    config_data = None
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            config_data = json.load(f)
    config = DictConfig(config_data)
    container.singleton(IConfig, config)

    # Register logger module
    app.use(LoggerModule())

    # Register logging middleware
    app.use_middleware(LoggingMiddleware(container))

    # Register user module
    app.use(UserModule())

    # Boot app
    app.boot(auto_discover="sagittarius_engine.extensions")
    print("Application booted successfully.")

    # Execute command
    user = app.dispatch(CreateUserCommand, {"id": 1, "name": "Alice"})
    print(f"Created user: {user.name}")

    user2 = app.dispatch(CreateUserCommand, {"id": 2, "name": "Bob"})

    # Execute query
    all_users = app.dispatch(ListUsersQuery)
    print(f"All users: {[u.name for u in all_users]}")

    # Graceful stop
    app.stop()


