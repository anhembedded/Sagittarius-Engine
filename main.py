from typing import Any
from src.core import App, BaseModule
from src.application.command_port import ICommand
from src.application.query_port import IQuery
from src.application.event_bus_port import IEventBus
from src.infra.stdlib_container_infra import Container

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
    app = App()
    app.use(UserModule())
    app.boot()

    # Execute command
    user = app.execute(CreateUserCommand, {'id': 1, 'name': 'Alice'})
    print(f"Created user: {user.name}")

    user2 = app.execute(CreateUserCommand, {'id': 2, 'name': 'Bob'})

    # Execute query
    all_users = app.query(ListUsersQuery)
    print(f"All users: {[u.name for u in all_users]}")