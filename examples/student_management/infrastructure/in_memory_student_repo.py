# Clean Architecture - Infrastructure Adapter (In-Memory Repository)
from typing import Sequence, Optional
from examples.student_management.application.contracts.student_repository import (
    IStudentRepository,
)
from examples.student_management.domain.student import Student


class InMemoryStudentRepository(IStudentRepository):
    def __init__(self) -> None:
        self._students: dict[str, Student] = {}

    def add(self, student: Student) -> Student:
        self._students[student.id] = student
        return student

    def update(self, student: Student) -> Student:
        self._students[student.id] = student
        return student

    def delete(self, uuid: str) -> None:
        self._students.pop(uuid, None)

    def get_by_id(self, uuid: str) -> Optional[Student]:
        return self._students.get(uuid)

    def get_by_student_id(self, student_id: str) -> Optional[Student]:
        for s in self._students.values():
            if s.student_id == student_id:
                return s
        return None

    def get_all(self) -> Sequence[Student]:
        return list(self._students.values())

    def search(self, term: str) -> Sequence[Student]:
        term_lower = term.lower()
        return [
            s
            for s in self._students.values()
            if term_lower in s.full_name.lower() or term_lower in s.student_id.lower()
        ]
