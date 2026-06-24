from src.base_module import BaseModule
from src.app_kernel import App
from example.simple_ui.application.get_hello_query import GetHelloQuery

class HelloModule(BaseModule):
    def register(self, app: App) -> None:
        app.container.bind(GetHelloQuery, GetHelloQuery)

    def boot(self, app: App) -> None:
        pass
