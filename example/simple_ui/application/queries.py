from src.interfaces import IQuery
from example.simple_ui.domain.i_user_repo import IUserRepository
from typing import List
from example.simple_ui.domain.user import User

class ListUsersQuery(IQuery):
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def execute(self, payload: None = None) -> List[User]:
        return self.repo.get_all()
