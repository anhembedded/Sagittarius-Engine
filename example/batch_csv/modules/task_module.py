from src.interfaces import IModule, IContainer, IEventBus
from example.batch_csv.domain.i_task_repo import ITaskRepository
from example.batch_csv.infrastructure.repo import MemoryTaskRepository

class TaskModule(IModule):
    def register(self, app) -> None:
        app.container.singleton(ITaskRepository, MemoryTaskRepository())

    def boot(self, app) -> None:
        app.event_bus.on("task.created", self.on_task_created)

    def on_task_created(self, task):
        print(f"[TaskModule] Received task.created event for task: {task.id} - {task.name}")
