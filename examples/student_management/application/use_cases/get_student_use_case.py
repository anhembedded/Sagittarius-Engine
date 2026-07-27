from examples.student_management.application.contracts.student_repository import IStudentRepository
from examples.student_management.application.dtos.queries import GetStudentQuery
from examples.student_management.domain.student import Student, StudentNotFoundError
from examples.student_management.application.contracts.use_case_ports import IGetStudentUseCase


class GetStudentUseCase(IGetStudentUseCase):
    def __init__(self, repo: IStudentRepository) -> None:
        self.repo = repo

    def execute(self, query: GetStudentQuery) -> Student:
        student = self.repo.get_by_id(query.id)
        if student is None:
            raise StudentNotFoundError(f"Student with ID '{query.id}' not found.")
        return student


# Alias for backward compatibility
GetStudentHandler = GetStudentUseCase
