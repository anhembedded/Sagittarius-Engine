from collections.abc import Sequence

from examples.student_management.application.contracts.student_repository import (
    IStudentRepository,
)
from examples.student_management.application.contracts.use_case_ports import (
    IListStudentsUseCase,
)
from examples.student_management.application.dtos.queries import ListStudentsQuery
from examples.student_management.domain.student import Student


class ListStudentsUseCase(IListStudentsUseCase):
    def __init__(self, repo: IStudentRepository) -> None:
        self.repo = repo

    def execute(self, query: ListStudentsQuery | None = None) -> Sequence[Student]:
        if query is None:
            query = ListStudentsQuery()
        return self.repo.get_all()


# Alias for backward compatibility
ListStudentsHandler = ListStudentsUseCase
