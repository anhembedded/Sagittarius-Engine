from src.core import BaseModule, App
from example.multi_module.application.create_user_command import CreateUserCommand

class UserModule(BaseModule):
    def register(self, app: App) -> None:
        app.container.bind(CreateUserCommand, CreateUserCommand)

    def boot(self, app: App) -> None:
        pass
