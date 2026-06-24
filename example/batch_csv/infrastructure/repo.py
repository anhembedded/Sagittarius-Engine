from typing import List
from example.batch_csv.domain.task import Task
from example.batch_csv.domain.i_task_repo import ITaskRepository

class MemoryTaskRepository(ITaskRepository):
    def __init__(self):
        self._tasks: List[Task] = []

    def save(self, task: Task) -> None:
        self._tasks.append(task)

    def get_all(self) -> List[Task]:
        return self._tasks
