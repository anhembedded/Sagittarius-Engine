from src.base_module import BaseModule
from src.app_kernel import App

class OrderModule(BaseModule):
    def register(self, app: App) -> None:
        pass

    def boot(self, app: App) -> None:
        # Listen to user module events
        app.event_bus.on('user.created', self.handle_user_created)

    def handle_user_created(self, user_data: dict) -> None:
        print(f"[OrderModule] Received user.created for User ID {user_data['id']}. Sending welcome discount!")
