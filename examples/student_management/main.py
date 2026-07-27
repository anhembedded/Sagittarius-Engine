import sys
import os

# Ensure the project root is in the python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from sagittarius_engine import App
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus


from sagittarius_engine.interfaces import IEventBus, IConfig, IContainer
from sagittarius_engine.infrastructure.config.dict_config import DictConfig

# Import Repository Interface & Implementation
from examples.student_management.app.contracts.student_repository import IStudentRepository
from examples.student_management.app.infrastructure.sqlite_student_repo import SqliteStudentRepository

# Import Handlers
from examples.student_management.app.handlers.add_student_handler import AddStudentCommandHandler
from examples.student_management.app.handlers.update_student_handler import UpdateStudentCommandHandler
from examples.student_management.app.handlers.delete_student_handler import DeleteStudentCommandHandler
from examples.student_management.app.handlers.list_students_handler import ListStudentsHandler
from examples.student_management.app.handlers.search_students_handler import SearchStudentsHandler
from examples.student_management.app.handlers.get_student_handler import GetStudentHandler
from examples.student_management.app.handlers.generate_report_handler import GenerateReportCommandHandler

# Import UI
from examples.student_management.app.ui.terminal_menu import TerminalMenu


def main() -> None:
    # 1. Initialize Dependency Injection Container and Event Bus
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    
    # 2. Instantiate App Facade
    app = App(container, event_bus)

    # 3. Register standard interfaces to DI container
    from sagittarius_engine.extensions.persistence.i_session import ISession
    from examples.student_management.app.infrastructure.mock_session import MockSession

    container.singleton(IContainer, container)
    container.singleton(IConfig, DictConfig(initial_data={"database.path": "students.db"}))
    container.singleton(IEventBus, event_bus)
    container.singleton(IStudentRepository, lambda c: c.resolve(SqliteStudentRepository))
    container.singleton(ISession, MockSession())




    # 4. Register Command/Query Handlers
    container.bind(AddStudentCommandHandler, AddStudentCommandHandler)
    container.bind(UpdateStudentCommandHandler, UpdateStudentCommandHandler)
    container.bind(DeleteStudentCommandHandler, DeleteStudentCommandHandler)
    container.bind(ListStudentsHandler, ListStudentsHandler)
    container.bind(SearchStudentsHandler, SearchStudentsHandler)
    container.bind(GetStudentHandler, GetStudentHandler)
    container.bind(GenerateReportCommandHandler, GenerateReportCommandHandler)

    # 4.1 Register Framework Middlewares on the Pipeline
    from sagittarius_engine.middleware.logging_middleware import LoggingMiddleware
    from sagittarius_engine.middleware.timing_middleware import TimingMiddleware
    from sagittarius_engine.middleware.validation_middleware import ValidationMiddleware
    from sagittarius_engine.middleware.transaction_middleware import TransactionMiddleware
    from examples.student_management.app.infrastructure.student_validation_middleware import StudentValidationMiddleware

    app.use_middleware(LoggingMiddleware(container))
    app.use_middleware(TimingMiddleware())
    app.use_middleware(ValidationMiddleware())
    app.use_middleware(TransactionMiddleware(container))
    app.use_middleware(StudentValidationMiddleware())

    # 4.2 Register Health Check Module
    from sagittarius_engine.extensions.health_module import HealthExtension
    app.use(HealthExtension())

    # 5. Register TerminalMenu as a Hosted Service
    menu = TerminalMenu(app)
    app.context.hosted_services.register(menu)

    # 5.1 Initialize QApplication and EventBridge for Desktop UI
    from PySide6.QtWidgets import QApplication
    from examples.student_management.app.ui.desktop_window import EventBridge, MainWindow

    qt_app = QApplication(sys.argv)
    bridge = EventBridge()

    # Intercept all EventBus events to log them universally to PySide6 UI log
    original_emit = event_bus.emit
    def logging_emit(event_name: str, data: Any = None):
        try:
            qt_inst = QApplication.instance()
            if qt_inst is not None:
                bridge.all_events_logged.emit(event_name, str(data) if data is not None else "")
        except Exception:
            pass
        original_emit(event_name, data)
    event_bus.emit = logging_emit

    # Map Sagittarius EventBus to Qt EventBridge signals
    event_bus.on("student.added", lambda s: bridge.student_added.emit(s))
    event_bus.on("student.updated", lambda s: bridge.student_updated.emit(s))
    event_bus.on("student.deleted", lambda s_id: bridge.student_deleted.emit(s_id))
    event_bus.on("report.progress", lambda p: bridge.report_progress.emit(p))
    event_bus.on("report.completed", lambda r: bridge.report_completed.emit(r))
    event_bus.on("health.updated", lambda h: bridge.health_updated.emit(h))

    # Register periodic background system health check (runs every 10 seconds)
    def run_periodic_health_check():
        try:
            from sagittarius_engine.extensions.health_check_query import HealthCheckQuery, HealthCheckDTO
            status = app.query(HealthCheckQuery, HealthCheckDTO())
            app.event_bus.emit("health.updated", status)
        except Exception:
            pass

    app.context.scheduler.every(seconds=10).do(run_periodic_health_check)

    # 6. Boot the App (which starts Terminal UI background thread and scheduler)
    try:
        app.boot()
    except Exception as e:
        print(f"❌ Failed to boot Sagittarius application: {e}")
        sys.exit(1)


    # 7. Start PySide6 Monitor Window on Main Thread
    window = MainWindow(app, bridge)
    window.show()

    # Run the Qt Event Loop on the Main Thread
    try:
        sys.exit(qt_app.exec())
    finally:
        # 8. Graceful Shutdown
        app.stop()




if __name__ == "__main__":
    main()
