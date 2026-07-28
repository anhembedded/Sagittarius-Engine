# Clean Architecture - MVP Pattern View Interface
from typing import Sequence, Any

from examples.student_management.domain.student import Student


class IStudentMonitorView:
    """
    # MVP Pattern - View Interface
    Abstract View contract defining presentation callbacks.
    The Presenter calls these methods to update the Passive View (PySide6 UI / CLI).
    """

    def display_students(self, students: Sequence[Student]) -> None:
        raise NotImplementedError

    def update_student_row(self, student: Student) -> None:
        raise NotImplementedError

    def remove_student_row(self, uuid: str) -> None:
        raise NotImplementedError

    def update_report_progress(self, progress: int) -> None:
        raise NotImplementedError

    def display_report(self, report_text: str) -> None:
        raise NotImplementedError

    def add_event_log(self, event_name: str, event_data: str) -> None:
        raise NotImplementedError

    def update_health_status(self, status: dict[str, Any]) -> None:
        raise NotImplementedError
