from example.CLI_smallApp.domain.user import User

class InMemoryUserRepository:
    def __init__(self):
        self._users: dict[str, User] = {}

    def save(self, user: User) -> None:
        self._users[user.id] = user

    def get_all(self) -> list[User]:
        return list(self._users.values())
