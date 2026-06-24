from src.interfaces import ICommand, IEventBus
from example.CLI_smallApp.infrastructure.user_repo import InMemoryUserRepository
from example.CLI_smallApp.domain.user import User

class CreateUserCommand(ICommand):
    def __init__(self, repo: InMemoryUserRepository, event_bus: IEventBus):
        self.repo = repo
        self.event_bus = event_bus

    def execute(self, input_dto: dict) -> User:
        user_id = input_dto.get("id")
        name = input_dto.get("name")
        user = User(user_id, name)
        self.repo.save(user)
        self.event_bus.emit('user.created', user)
        return user
