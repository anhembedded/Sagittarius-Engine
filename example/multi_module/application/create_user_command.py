from src.core import ICommand, IEventBus

class CreateUserCommand(ICommand):
    def __init__(self, event_bus: IEventBus):
        self.event_bus = event_bus

    def execute(self, user_data: dict) -> None:
        print(f"[UserModule] Creating user: {user_data['name']}")
        user_id = 123 # Mock ID
        user_data['id'] = user_id
        self.event_bus.emit('user.created', user_data)
