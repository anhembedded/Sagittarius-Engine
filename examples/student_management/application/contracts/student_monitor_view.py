# Clean Architecture - MVP Pattern View Interface
from abc import ABC, abstractmethod
from typing import Sequence, Any

from examples.student_management.domain.student import Student


class IStudentMonitorView(ABC):
    """
    # MVP Pattern - View Interface
    Abstract View contract defining presentation callbacks.
    The Presenter calls these methods to update the Passive View (PySide6 UI / CLI).
    """

    @abstractmethod
    def display_students(self, students: Sequence[Student]) -> None: ...

    @abstractmethod
    def update_student_row(self, student: Student) -> None: ...

    @abstractmethod
    def remove_student_row(self, uuid: str) -> None: ...

    @abstractmethod
    def update_report_progress(self, progress: int) -> None: ...

    @abstractmethod
    def display_report(self, report_text: str) -> None: ...

    @abstractmethod
    def add_event_log(self, event_name: str, event_data: str) -> None: ...

    @abstractmethod
    def update_health_status(self, status: dict[str, Any]) -> None: ...
