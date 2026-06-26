from dataclasses import dataclass
from src.interfaces import ICommand, IEventBus

@dataclass
class CreateUserDto:
    username: str
    email: str

class CreateUserCommand(ICommand):
    def __init__(self, event_bus: IEventBus):
        self.event_bus = event_bus

    def execute(self, data_transfer_obj: CreateUserDto) -> dict:
        # In a real app, you would save this user to a repo
        print(f"[UserModule] Created user: {data_transfer_obj.username}")

        # Emit an event that the user was created
        self.event_bus.emit('user.created', data_transfer_obj.email)
        return {"status": "success", "username": data_transfer_obj.username}
