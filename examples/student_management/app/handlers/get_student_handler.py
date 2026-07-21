from sagittarius_engine.extensions.cqrs.queries import IQuery
from examples.student_management.app.contracts.student_repository import IStudentRepository
from examples.student_management.app.queries.get_student import GetStudentQuery
from examples.student_management.app.models.student import Student, StudentNotFoundError


class GetStudentHandler(IQuery):
    def __init__(self, repo: IStudentRepository) -> None:
        self.repo = repo

    def execute(self, query: GetStudentQuery) -> Student:
        student = self.repo.get_by_id(query.id)
        if student is None:
            raise StudentNotFoundError(f"Student with ID '{query.id}' not found.")
        return student
