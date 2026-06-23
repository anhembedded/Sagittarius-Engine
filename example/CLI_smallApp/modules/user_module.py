from src.core import BaseModule, App
from src.application.command_port import ICommand
from src.application.query_port import IQuery
from example.CLI_smallApp.domain.user import UserRepositoryPort
from example.CLI_smallApp.infrastructure.memory_repo import MemoryUserRepository
from example.CLI_smallApp.application.commands import CreateUserCommand
from example.CLI_smallApp.application.queries import ListUsersQuery

class UserModule(BaseModule):
    def register(self, app: App) -> None:
        # Register Infrastructure
        app.container.singleton(UserRepositoryPort, MemoryUserRepository())

        # Register Use Cases
        app.container.bind(CreateUserCommand, CreateUserCommand)
        app.container.bind(ListUsersQuery, ListUsersQuery)

    def boot(self, app: App) -> None:
        # Subscribe to domain events
        def on_user_created(data: dict):
            print(f"\n[EVENT] user.created emitted for {data['name']} (ID: {data['user_id']})")

        app.event_bus.on("user.created", on_user_created)
