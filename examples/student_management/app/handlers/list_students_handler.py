from typing import List
from sagittarius_engine.extensions.cqrs.queries import IQuery
from examples.student_management.app.contracts.student_repository import IStudentRepository
from examples.student_management.app.queries.list_students import ListStudentsQuery
from examples.student_management.app.models.student import Student


class ListStudentsHandler(IQuery):
    def __init__(self, repo: IStudentRepository) -> None:
        self.repo = repo

    def execute(self, query: ListStudentsQuery) -> List[Student]:
        return self.repo.get_all()
