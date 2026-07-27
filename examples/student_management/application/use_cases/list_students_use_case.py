from typing import Sequence
from examples.student_management.application.contracts.student_repository import IStudentRepository
from examples.student_management.application.dtos.queries import ListStudentsQuery
from examples.student_management.domain.student import Student
from sagittarius_engine.extensions.cqrs import IQuery
from examples.student_management.application.contracts.use_case_ports import IListStudentsUseCase


class ListStudentsUseCase(IListStudentsUseCase):
    def __init__(self, repo: IStudentRepository) -> None:
        self.repo = repo

    def execute(self, query: ListStudentsQuery = ListStudentsQuery()) -> Sequence[Student]:
        return self.repo.get_all()


# Alias for backward compatibility
ListStudentsHandler = ListStudentsUseCase
