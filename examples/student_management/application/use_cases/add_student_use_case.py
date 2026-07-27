# Clean Architecture - UseCase (Command Handler)
import uuid
from examples.student_management.application.contracts.student_repository import IStudentRepository
from examples.student_management.application.dtos.commands import AddStudentCommand
from examples.student_management.domain.student import Student, DuplicateStudentIDError
from sagittarius_engine.extensions.cqrs import ICommand
from sagittarius_engine.interfaces import IEventBus


class AddStudentUseCase(ICommand[AddStudentCommand, Student]):
    def __init__(self, repo: IStudentRepository, event_bus: IEventBus) -> None:
        self.repo = repo
        self.event_bus = event_bus

    def execute(self, command: AddStudentCommand) -> Student:
        existing = self.repo.get_by_student_id(command.student_id)
        if existing is not None:
            raise DuplicateStudentIDError(
                f"Student ID '{command.student_id}' already exists."
            )

        student = Student(
            id=str(uuid.uuid4()),
            student_id=command.student_id,
            full_name=command.full_name,
            age=command.age,
            gender=command.gender,
            major=command.major,
            gpa=command.gpa,
        )
        self.repo.add(student)
        self.event_bus.emit("student.added", student)
        return student


# Alias for backward compatibility with CQRS Handler resolution
AddStudentCommandHandler = AddStudentUseCase
