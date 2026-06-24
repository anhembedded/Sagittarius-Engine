from src.interfaces import IModule
from src.app_kernel import App
from example.CLI_smallApp.application.commands import CreateUserCommand
from example.CLI_smallApp.application.queries import ListUsersQuery
from example.CLI_smallApp.infrastructure.user_repo import InMemoryUserRepository

class UserModule(IModule):
    def register(self, app: App) -> None:
        # Register dependencies
        app.container.singleton(InMemoryUserRepository, InMemoryUserRepository())
        app.container.bind(CreateUserCommand, CreateUserCommand)
        app.container.bind(ListUsersQuery, ListUsersQuery)

    def boot(self, app: App) -> None:
        def on_user_created(user):
            print(f"[EventBus] UserCreated handled! Log: user {user.id} - {user.name} was created.")

        app.event_bus.on('user.created', on_user_created)
