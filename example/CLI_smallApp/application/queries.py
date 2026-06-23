from typing import List
from src.application.query_port import IQuery
from example.CLI_smallApp.domain.user import User, UserRepositoryPort

class ListUsersQuery(IQuery):
    def __init__(self, repo: UserRepositoryPort):
        self.repo = repo

    def execute(self, _=None) -> List[User]:
        return self.repo.list_all()
