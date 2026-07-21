from sagittarius_engine.extensions.cqrs.commands import ICommand
from sagittarius_engine.interfaces import IEventBus
from examples.student_management.app.contracts.student_repository import IStudentRepository
from examples.student_management.app.commands.delete_student import DeleteStudentCommand
from examples.student_management.app.models.student import StudentNotFoundError


class DeleteStudentCommandHandler(ICommand):
    def __init__(self, repo: IStudentRepository, event_bus: IEventBus) -> None:
        self.repo = repo
        self.event_bus = event_bus

    def execute(self, command: DeleteStudentCommand) -> None:
        student = self.repo.get_by_id(command.id)
        if student is None:
            raise StudentNotFoundError(f"Student with ID '{command.id}' not found.")
        self.repo.delete(command.id)
        self.event_bus.emit("student.deleted", command.id)

