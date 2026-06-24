from dataclasses import dataclass
from src.interfaces import ICommand, IEventBus

@dataclass
class CreateUserDto:
    username: str
    email: str

class CreateUserCommand(ICommand):
    def __init__(self, event_bus: IEventBus):
        self.event_bus = event_bus

    def execute(self, dto: CreateUserDto) -> dict:
        # In a real app, you would save this user to a repo
        print(f"[UserModule] Created user: {dto.username}")

        # Emit an event that the user was created
        self.event_bus.emit('user.created', dto.email)
        return {"status": "success", "username": dto.username}
