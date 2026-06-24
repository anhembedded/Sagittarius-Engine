import abc
from typing import List
from example.batch_csv.domain.task import Task

class ITaskRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, task: Task) -> None:
        pass

    @abc.abstractmethod
    def get_all(self) -> List[Task]:
        pass
