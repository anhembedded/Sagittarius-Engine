from src.base_module import BaseModule
from src.app_kernel import App
from example.multi_module.application.create_user_command import CreateUserCommand

class UserModule(BaseModule):
    def register(self, app: App) -> None:
        app.container.bind(CreateUserCommand, CreateUserCommand)

    def boot(self, app: App) -> None:
        pass
