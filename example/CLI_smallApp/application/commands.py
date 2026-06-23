from dataclasses import dataclass
from src.application.command_port import ICommand
from src.application.event_bus_port import IEventBus
from example.CLI_smallApp.domain.user import User, UserRepositoryPort

@dataclass
class CreateUserDto:
    user_id: str
    name: str

class CreateUserCommand(ICommand):
    def __init__(self, repo: UserRepositoryPort, event_bus: IEventBus):
        self.repo = repo
        self.event_bus = event_bus

    def execute(self, dto: CreateUserDto) -> None:
        user = User(dto.user_id, dto.name)
        self.repo.save(user)
        self.event_bus.emit("user.created", {"user_id": user.user_id, "name": user.name})
