# Clean Architecture - Domain Events
from sagittarius_engine.domain import BaseEvent
from examples.student_management.domain.student import Student


class StudentAddedEvent(BaseEvent):
    event_name = "student.added"

    def __init__(self, student: Student) -> None:
        super().__init__()
        self.student = student


class StudentUpdatedEvent(BaseEvent):
    event_name = "student.updated"

    def __init__(self, student: Student) -> None:
        super().__init__()
        self.student = student


class StudentDeletedEvent(BaseEvent):
    event_name = "student.deleted"

    def __init__(self, student_id: str) -> None:
        super().__init__()
        self.student_id = student_id


class ReportCompletedEvent(BaseEvent):
    event_name = "report.completed"

    def __init__(self, report_content: str) -> None:
        super().__init__()
        self.report_content = report_content
