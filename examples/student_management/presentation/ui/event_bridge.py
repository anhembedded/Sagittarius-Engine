# Clean Architecture - Presentation Layer (Qt Event Bridge)
from PySide6.QtCore import QObject, Signal


class EventBridge(QObject):
    """
    @brief Qt QObject used as a thread-safe signal bridge.
    @details Sagittarius event bus callbacks are run on worker/async threads.
    We marshall those events onto the Qt GUI thread using Qt Signals and Slots.
    """

    student_added = Signal(object)
    student_updated = Signal(object)
    student_deleted = Signal(str)
    report_progress = Signal(int)
    report_completed = Signal(str)
    all_events_logged = Signal(str, str)  # universal log: event_name, event_data
    health_updated = Signal(object)  # dict containing health query results
