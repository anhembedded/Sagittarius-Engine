# Concrete In-Memory Student Repository Implementation
import threading
from typing import List, Optional
from examples.student_management.app.contracts.student_repository import IStudentRepository
from examples.student_management.app.models.student import Student


class InMemoryStudentRepository(IStudentRepository):
    def __init__(self) -> None:
        self._students: dict[str, Student] = {}
        self._lock = threading.Lock()

    def add(self, student: Student) -> None:
        with self._lock:
            self._students[student.id] = student

    def update(self, student: Student) -> None:
        with self._lock:
            if student.id in self._students:
                self._students[student.id] = student

    def delete(self, student_id_or_uuid: str) -> None:
        with self._lock:
            # Check UUID first
            if student_id_or_uuid in self._students:
                del self._students[student_id_or_uuid]
                return
            # Otherwise search by student ID
            for uuid, student in list(self._students.items()):
                if student.student_id == student_id_or_uuid:
                    del self._students[uuid]
                    break

    def get_by_id(self, uuid: str) -> Optional[Student]:
        with self._lock:
            return self._students.get(uuid)

    def get_by_student_id(self, student_id: str) -> Optional[Student]:
        with self._lock:
            for student in self._students.values():
                if student.student_id == student_id:
                    return student
            return None

    def get_all(self) -> List[Student]:
        with self._lock:
            return list(self._students.values())

    def search_by_name(self, name: str) -> List[Student]:
        with self._lock:
            name_lower = name.lower()
            return [
                student
                for student in self._students.values()
                if name_lower in student.full_name.lower()
            ]
