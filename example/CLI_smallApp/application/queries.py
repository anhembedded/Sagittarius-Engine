from src.interfaces import IQuery
from example.CLI_smallApp.infrastructure.user_repo import InMemoryUserRepository

class ListUsersQuery(IQuery):
    def __init__(self, repo: InMemoryUserRepository):
        self.repo = repo

    def execute(self, input_dto: dict = None) -> list:
        return self.repo.get_all()
