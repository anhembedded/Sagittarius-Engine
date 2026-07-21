from typing import List
from sagittarius_engine.extensions.cqrs.queries import IQuery
from examples.student_management.app.contracts.student_repository import IStudentRepository
from examples.student_management.app.queries.search_students import SearchStudentsQuery
from examples.student_management.app.models.student import Student


class SearchStudentsHandler(IQuery):
    def __init__(self, repo: IStudentRepository) -> None:
        self.repo = repo

    def execute(self, query: SearchStudentsQuery) -> List[Student]:
        # Search by student ID first for exact matches
        student = self.repo.get_by_student_id(query.term)
        if student is not None:
            return [student]
        # Otherwise search by name
        return self.repo.search_by_name(query.term)
