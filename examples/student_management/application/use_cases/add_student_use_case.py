# Clean Architecture - UseCase (Command Handler)
import uuid
from examples.student_management.application.contracts.student_repository import (
    IStudentRepository,
)
from examples.student_management.application.dtos.commands import AddStudentCommand
from examples.student_management.domain.student import Student, DuplicateStudentIDError
from sagittarius_engine.interfaces import IEventBus, ILogger
from examples.student_management.application.contracts.use_case_ports import (
    IAddStudentUseCase,
)


class AddStudentUseCase(IAddStudentUseCase):
    def __init__(
        self,
        repo: IStudentRepository,
        event_bus: IEventBus,
        logger: ILogger,
    ) -> None:
        self.repo = repo
        self.event_bus = event_bus
        self.logger = logger

    def execute(self, command: AddStudentCommand) -> Student:
        self.logger.info(
            f"Adding student: student_id='{command.student_id}' name='{command.full_name}'"
        )

        existing = self.repo.get_by_student_id(command.student_id)
        if existing is not None:
            self.logger.warning(
                f"Duplicate student ID rejected: '{command.student_id}'"
            )
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
        self.logger.info(
            f"Student added successfully: id='{student.id}' student_id='{student.student_id}'"
        )
        return student


# Alias for backward compatibility with CQRS Handler resolution
AddStudentCommandHandler = AddStudentUseCase
