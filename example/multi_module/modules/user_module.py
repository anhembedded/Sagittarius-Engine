from src.interfaces import IModule, IContainer

class UserModule(IModule):
    def register(self, app) -> None:
        pass

    def boot(self, app) -> None:
        pass
