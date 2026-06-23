from typing import List
from example.CLI_smallApp.domain.user import User, UserRepositoryPort

class MemoryUserRepository(UserRepositoryPort):
    def __init__(self) -> None:
        self._users: List[User] = []

    def save(self, user: User) -> None:
        self._users.append(user)

    def list_all(self) -> List[User]:
        return self._users.copy()
