# Clean Architecture - MVP Pattern (Presenter)
from typing import Any
from sagittarius_engine import App
from sagittarius_engine.interfaces import IEventBus
from examples.student_management.application.contracts.student_monitor_view import IStudentMonitorView
from examples.student_management.application.contracts.student_repository import IStudentRepository
from examples.student_management.domain.student import Student


class StudentMonitorPresenter:
    """
    # MVP Pattern - Presenter
    The Presenter acts as the mediator between the IStudentMonitorView (Passive View)
    and the Application Use Cases / EventBus.
    Contains zero PySide6/GUI framework dependencies.
    """

    def __init__(self, view: IStudentMonitorView, app: App) -> None:
        self.view = view
        self.app = app
        self.repo: IStudentRepository = app.container.resolve(IStudentRepository)
        self.event_bus: IEventBus = app.container.resolve(IEventBus)

    def initialize(self) -> None:
        """
        Loads initial dataset and binds presentation listeners.
        """
        self.load_initial_students()

    def load_initial_students(self) -> None:
        students = self.repo.get_all()
        self.view.display_students(students)

    def on_student_added(self, student: Student) -> None:
        self.view.update_student_row(student)

    def on_student_updated(self, student: Student) -> None:
        self.view.update_student_row(student)

    def on_student_deleted(self, uuid: str) -> None:
        self.view.remove_student_row(uuid)

    def on_report_progress(self, progress: int) -> None:
        self.view.update_report_progress(progress)

    def on_report_completed(self, report_content: str) -> None:
        self.view.display_report(report_content)

    def on_event_logged(self, event_name: str, event_data: str) -> None:
        self.view.add_event_log(event_name, event_data)

    def on_health_updated(self, status: dict[str, Any]) -> None:
        self.view.update_health_status(status)
