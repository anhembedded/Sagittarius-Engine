from dataclasses import dataclass
from src.interfaces import ICommand
from example.simple_ui.domain.user import User
from example.simple_ui.domain.i_user_repo import IUserRepository
import uuid

@dataclass
class CreateUserDto:
    username: str

class CreateUserCommand(ICommand):
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def execute(self, dto: CreateUserDto) -> User:
        user = User(id=str(uuid.uuid4()), username=dto.username)
        self.repo.save(user)
        return user
