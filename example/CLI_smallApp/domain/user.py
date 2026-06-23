from abc import ABC, abstractmethod
from typing import List

class User:
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name

    def __repr__(self) -> str:
        return f"User(id={self.user_id}, name={self.name})"

class UserRepositoryPort(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        ...

    @abstractmethod
    def list_all(self) -> List[User]:
        ...
