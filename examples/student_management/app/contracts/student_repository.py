# Student Repository Interface
from abc import ABC, abstractmethod
from typing import Optional, List
from examples.student_management.app.models.student import Student


class IStudentRepository(ABC):
    @abstractmethod
    def add(self, student: Student) -> None:
        ...

    @abstractmethod
    def update(self, student: Student) -> None:
        ...

    @abstractmethod
    def delete(self, student_id_or_uuid: str) -> None:
        ...

    @abstractmethod
    def get_by_id(self, uuid: str) -> Optional[Student]:
        ...

    @abstractmethod
    def get_by_student_id(self, student_id: str) -> Optional[Student]:
        ...

    @abstractmethod
    def get_all(self) -> List[Student]:
        ...

    @abstractmethod
    def search_by_name(self, name: str) -> List[Student]:
        ...
