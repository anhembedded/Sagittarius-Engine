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

    def execute(self, dto: CreateTaskDto) -> None:
        task = Task(id=dto.id, name=dto.name)
        self.repo.save(task)
        self.event_bus.emit('task.created', task)
