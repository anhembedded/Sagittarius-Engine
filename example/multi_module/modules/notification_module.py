from src.interfaces import IModule

class NotificationModule(IModule):
    def register(self, app) -> None:
        pass

    def boot(self, app) -> None:
        # Listen to the event emitted by UserModule
        app.event_bus.on("user.created", self.on_user_created)

    def on_user_created(self, email: str) -> None:
        print(f"[NotificationModule] Received user.created event. Sending welcome email to {email}")
