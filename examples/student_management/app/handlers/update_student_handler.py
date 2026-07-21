from sagittarius_engine.extensions.cqrs.commands import ICommand
from sagittarius_engine.interfaces import IEventBus
from examples.student_management.app.contracts.student_repository import IStudentRepository
from examples.student_management.app.commands.update_student import UpdateStudentCommand
from examples.student_management.app.models.student import (
    Student,
    StudentNotFoundError,
    DuplicateStudentIDError,
)


class UpdateStudentCommandHandler(ICommand):
    def __init__(self, repo: IStudentRepository, event_bus: IEventBus) -> None:
        self.repo = repo
        self.event_bus = event_bus

    def execute(self, command: UpdateStudentCommand) -> Student:
        student = self.repo.get_by_id(command.id)
        if student is None:
            raise StudentNotFoundError(f"Student with ID '{command.id}' not found.")

        # If student ID is being changed, check if new ID already conflicts with another student
        if command.student_id != student.student_id:
            existing = self.repo.get_by_student_id(command.student_id)
            if existing is not None:
                raise DuplicateStudentIDError(
                    f"Student ID '{command.student_id}' already exists."
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
        self.event_bus.emit("student.updated", updated_student)
        return updated_student

