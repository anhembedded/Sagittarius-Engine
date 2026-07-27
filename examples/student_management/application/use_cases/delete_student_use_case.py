# Clean Architecture - UseCase (Command Handler)
from examples.student_management.application.contracts.student_repository import IStudentRepository
from examples.student_management.application.dtos.commands import DeleteStudentCommand
from examples.student_management.domain.student import StudentNotFoundError
from sagittarius_engine.extensions.cqrs import ICommand
from sagittarius_engine.interfaces import IEventBus


class DeleteStudentUseCase(ICommand[DeleteStudentCommand, None]):
    def __init__(self, repo: IStudentRepository, event_bus: IEventBus) -> None:
        self.repo = repo
        self.event_bus = event_bus

    def execute(self, command: DeleteStudentCommand) -> None:
        existing = self.repo.get_by_id(command.id)
        if existing is None:
            raise StudentNotFoundError(f"Student with ID '{command.id}' not found.")

        self.repo.delete(command.id)
        self.event_bus.emit("student.deleted", command.id)


# Alias for backward compatibility
DeleteStudentCommandHandler = DeleteStudentUseCase
