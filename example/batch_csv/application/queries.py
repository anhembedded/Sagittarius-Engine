from src.interfaces import IQuery
from example.batch_csv.domain.i_task_repo import ITaskRepository
from typing import List
from example.batch_csv.domain.task import Task

class ListTasksQuery(IQuery):
    def __init__(self, repo: ITaskRepository):
        self.repo = repo

    def execute(self, payload: None = None) -> List[Task]:
        return self.repo.get_all()
