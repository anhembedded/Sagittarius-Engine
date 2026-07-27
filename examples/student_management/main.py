import sys
import os
from typing import Any

# Ensure project root is in python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from sagittarius_engine import App
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from sagittarius_engine.infrastructure.config.dict_config import DictConfig
from sagittarius_engine.interfaces import IEventBus, IConfig, IContainer

from examples.student_management.student_module import StudentModule
from examples.student_management.presentation.cli.terminal_menu import TerminalMenu
from examples.student_management.presentation.ui.desktop_window import EventBridge, MainWindow


def main() -> None:
    # 1. Initialize Composition Root Core
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    # 2. Bind Infrastructure Core Singletons
    config = DictConfig(
        initial_data={
            "database.path": "students.db",
            "log.level": "INFO",
            "log.file": "student_app.log",
            "log.viewer.enabled": True,
            "log.viewer.host": "localhost",
            "log.viewer.port": 9999,
            "log.viewer.module": "student-management",
        }
    )
    container.singleton(IConfig, config)
    container.singleton(IEventBus, event_bus)
    container.singleton(IContainer, container)

    # 3. Add Logger Module
    from sagittarius_engine.extensions.logger_module import LoggerExtension
    app.use(LoggerExtension())

    # 4. Use Student Module & Health Extension
    app.use(StudentModule())

    from sagittarius_engine.extensions.health_module import HealthExtension
    app.use(HealthExtension())

    # 5. Register TerminalMenu Hosted Service
    menu = TerminalMenu(app)
    app.context.hosted_services.register(menu)

    # 6. Initialize PySide6 GUI & Thread-Safe EventBridge
    from PySide6.QtWidgets import QApplication
    qt_app = QApplication(sys.argv)
    bridge = EventBridge()

    # Intercept all EventBus events to log them universally to PySide6 UI log panel
    original_emit = event_bus.emit
    def logging_emit(event_name: str, data: Any = None):
        try:
            qt_inst = QApplication.instance()
            if qt_inst is not None:
                bridge.all_events_logged.emit(event_name, str(data) if data is not None else "")
        except Exception:
            pass
        original_emit(event_name, data)
    setattr(event_bus, "emit", logging_emit)

    # Wire Sagittarius EventBus signals to Qt EventBridge
    event_bus.on("student.added", lambda s: bridge.student_added.emit(s))
    event_bus.on("student.updated", lambda s: bridge.student_updated.emit(s))
    event_bus.on("student.deleted", lambda s_id: bridge.student_deleted.emit(s_id))
    event_bus.on("report.progress", lambda p: bridge.report_progress.emit(p))
    event_bus.on("report.completed", lambda r: bridge.report_completed.emit(r))
    event_bus.on("health.updated", lambda status: bridge.health_updated.emit(status))

    # 7. Create MVP View & Presenter (MainWindow implements IStudentMonitorView)
    window = MainWindow(app, bridge)
    window.show()

    # 8. Boot Application Kernel
    app.boot()

    # 9. Run Qt Event Loop
    try:
        sys.exit(qt_app.exec())
    finally:
        app.stop()


if __name__ == "__main__":
    main()
