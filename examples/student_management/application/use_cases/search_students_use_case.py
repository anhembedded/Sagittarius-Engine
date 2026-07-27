from typing import Sequence
from examples.student_management.application.contracts.student_repository import IStudentRepository
from examples.student_management.application.dtos.queries import SearchStudentsQuery
from examples.student_management.domain.student import Student
from sagittarius_engine.extensions.cqrs import IQuery


class SearchStudentsUseCase(IQuery[SearchStudentsQuery, Sequence[Student]]):
    def __init__(self, repo: IStudentRepository) -> None:
        self.repo = repo

    def execute(self, query: SearchStudentsQuery) -> Sequence[Student]:
        return self.repo.search(query.term)


# Alias for backward compatibility
SearchStudentsHandler = SearchStudentsUseCase
