# Clean Architecture - Application Port (Repository Interface)
from abc import ABC, abstractmethod
from typing import Sequence

from examples.student_management.domain.student import Student


class IStudentRepository(ABC):
    """
    Abstract Output Port for Student Persistence.
    """

    @abstractmethod
    def add(self, student: Student) -> Student: ...

    @abstractmethod
    def update(self, student: Student) -> Student: ...

    @abstractmethod
    def delete(self, uuid: str) -> None: ...

    @abstractmethod
    def get_by_id(self, uuid: str) -> Student | None: ...

    @abstractmethod
    def get_by_student_id(self, student_id: str) -> Student | None: ...

    @abstractmethod
    def get_all(self) -> Sequence[Student]: ...

    @abstractmethod
    def search(self, term: str) -> Sequence[Student]: ...
