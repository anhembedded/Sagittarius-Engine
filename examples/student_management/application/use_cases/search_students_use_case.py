from typing import Sequence
from examples.student_management.application.contracts.student_repository import (
    IStudentRepository,
)
from examples.student_management.application.dtos.queries import SearchStudentsQuery
from examples.student_management.domain.student import Student
from examples.student_management.application.contracts.use_case_ports import (
    ISearchStudentsUseCase,
)


class SearchStudentsUseCase(ISearchStudentsUseCase):
    def __init__(self, repo: IStudentRepository) -> None:
        self.repo = repo

    def execute(self, query: SearchStudentsQuery) -> Sequence[Student]:
        return self.repo.search(query.term)


# Alias for backward compatibility
SearchStudentsHandler = SearchStudentsUseCase
