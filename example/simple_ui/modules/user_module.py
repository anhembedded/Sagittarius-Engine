from src.interfaces import IModule
from example.simple_ui.domain.i_user_repo import IUserRepository
from example.simple_ui.infrastructure.user_repo import MemoryUserRepository

class UserModule(IModule):
    def register(self, app) -> None:
        app.container.singleton(IUserRepository, MemoryUserRepository())

    def boot(self, app) -> None:
        pass
