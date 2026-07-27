# Clean Architecture - Domain Events
from sagittarius_engine.base import BaseEvent
from examples.student_management.domain.student import Student


class StudentAddedEvent(BaseEvent):
    def __init__(self, student: Student) -> None:
        super().__init__()
        self.student = student


class StudentUpdatedEvent(BaseEvent):
    def __init__(self, student: Student) -> None:
        super().__init__()
        self.student = student


class StudentDeletedEvent(BaseEvent):
    def __init__(self, student_id: str) -> None:
        super().__init__()
        self.student_id = student_id


class ReportCompletedEvent(BaseEvent):
    def __init__(self, report_content: str) -> None:
        super().__init__()
        self.report_content = report_content
