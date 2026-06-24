from typing import List
from example.simple_ui.domain.user import User
from example.simple_ui.domain.i_user_repo import IUserRepository

class MemoryUserRepository(IUserRepository):
    def __init__(self):
        self._users: List[User] = []

    def save(self, user: User) -> None:
        self._users.append(user)

    def get_all(self) -> List[User]:
        return self._users
