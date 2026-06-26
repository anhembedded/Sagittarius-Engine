from dataclasses import dataclass
from src.interfaces import ICommand, IEventBus
from example.batch_csv.domain.task import Task
from example.batch_csv.domain.i_task_repo import ITaskRepository

@dataclass
class CreateTaskDto:
    id: str
    name: str

class CreateTaskCommand(ICommand):
    def __init__(self, repo: ITaskRepository, event_bus: IEventBus):
        self.repo = repo
        self.event_bus = event_bus

    def execute(self, data_transfer_obj: CreateTaskDto) -> None:
        task = Task(id=data_transfer_obj.id, name=data_transfer_obj.name)
        self.repo.save(task)
        self.event_bus.emit('task.created', task)
