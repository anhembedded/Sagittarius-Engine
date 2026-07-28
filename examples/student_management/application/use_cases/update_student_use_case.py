# Clean Architecture - UseCase (Command Handler)
from examples.student_management.application.contracts.student_repository import (
    IStudentRepository,
)
from examples.student_management.application.dtos.commands import UpdateStudentCommand
from examples.student_management.domain.events import StudentUpdatedEvent
from examples.student_management.domain.student import (
    Student,
    StudentNotFoundError,
    DuplicateStudentIDError,
)
from sagittarius_engine.interfaces import IEventBus
from examples.student_management.application.contracts.use_case_ports import (
    IUpdateStudentUseCase,
)


class UpdateStudentUseCase(IUpdateStudentUseCase):
    def __init__(self, repo: IStudentRepository, event_bus: IEventBus) -> None:
        self.repo = repo
        self.event_bus = event_bus

    def execute(self, command: UpdateStudentCommand) -> Student:
        existing = self.repo.get_by_id(command.id)
        if existing is None:
            raise StudentNotFoundError(f"Student with ID '{command.id}' not found.")

        # Check duplicate student_id if changed
        if command.student_id != existing.student_id:
            other = self.repo.get_by_student_id(command.student_id)
            if other is not None and other.id != command.id:
                raise DuplicateStudentIDError(
                    f"Student ID '{command.student_id}' is already in use."
                )

        updated_student = Student(
            id=command.id,
            student_id=command.student_id,
            full_name=command.full_name,
            age=command.age,
            gender=command.gender,
            major=command.major,
            gpa=command.gpa,
        )

        self.repo.update(updated_student)
        self.event_bus.emit(StudentUpdatedEvent(updated_student))
        return updated_student


# Alias for backward compatibility
UpdateStudentCommandHandler = UpdateStudentUseCase
