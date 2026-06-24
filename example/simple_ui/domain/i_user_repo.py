import abc
from typing import List
from example.simple_ui.domain.user import User

class IUserRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, user: User) -> None:
        pass

    @abc.abstractmethod
    def get_all(self) -> List[User]:
        pass
