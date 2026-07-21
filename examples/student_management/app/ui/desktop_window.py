from typing import Any
import sys
from PySide6.QtCore import QObject, Signal, Slot, Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QProgressBar,
    QListWidget,
    QHeaderView,
)
from PySide6.QtGui import QFont, QColor
from sagittarius_engine import App
from examples.student_management.app.contracts.student_repository import IStudentRepository
from examples.student_management.app.models.student import Student


class EventBridge(QObject):
    """
    @brief Qt QObject used as a thread-safe signal bridge.
    @details Sagittarius event bus callbacks are run on worker/async threads.
    We marshalls those events onto the Qt GUI thread using Qt Signals and Slots.
    """

    student_added = Signal(object)
    student_updated = Signal(object)
    student_deleted = Signal(str)
    report_progress = Signal(int)
    report_completed = Signal(str)
    all_events_logged = Signal(str, str)  # universal log: event_name, event_data
    health_updated = Signal(object)  # dict containing health query results


class MainWindow(QMainWindow):
    def __init__(self, app: App, bridge: EventBridge) -> None:
        super().__init__()
        self.app = app
        self.bridge = bridge
        self.repo = app.container.resolve(IStudentRepository)

        self.setWindowTitle("Sagittarius Engine - Student Monitor (PySide6)")
        self.resize(1150, 700)
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #1e222b;
            }
            QWidget {
                color: #abb2bf;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
            }
            QLabel {
                font-weight: bold;
            }
            QTableWidget {
                background-color: #21252b;
                gridline-color: #2c313c;
                border: 1px solid #181a1f;
                selection-background-color: #3e4451;
                selection-color: #ffffff;
            }
            QHeaderView::section {
                background-color: #282c34;
                color: #abb2bf;
                padding: 6px;
                border: 1px solid #181a1f;
                font-weight: bold;
            }
            QListWidget {
                background-color: #21252b;
                border: 1px solid #181a1f;
                padding: 5px;
            }
            QProgressBar {
                border: 1px solid #3e4451;
                border-radius: 4px;
                text-align: center;
                background-color: #21252b;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #61afef;
                border-radius: 3px;
            }
            QStatusBar {
                background-color: #21252b;
                border-top: 1px solid #181a1f;
            }
            """
        )

        self._init_ui()
        self._load_existing_students()
        self._connect_signals()

    def _init_ui(self) -> None:
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # --- LEFT PANEL: Student Database Table ---
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        table_title = QLabel("📂 STUDENT DATABASE")
        table_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        table_title.setStyleSheet("color: #61afef; margin-bottom: 5px;")
        left_layout.addWidget(table_title)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["Internal UUID", "Student ID", "Full Name", "Age", "Gender", "Major", "GPA"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        left_layout.addWidget(self.table)

        main_layout.addWidget(left_widget, stretch=7)

        # --- RIGHT PANEL: Real-time Monitor Logs & Progress ---
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(12)

        # Log Header
        log_title = QLabel("⚡ UNIVERSAL EVENT BUS LOGS")
        log_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        log_title.setStyleSheet("color: #61afef;")
        right_layout.addWidget(log_title)

        self.log_list = QListWidget()
        right_layout.addWidget(self.log_list)

        # Progress Header
        progress_title = QLabel("📊 GPA ANALYTICS REPORT (ASYNC)")
        progress_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        progress_title.setStyleSheet("color: #e5c07b;")
        right_layout.addWidget(progress_title)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        right_layout.addWidget(self.progress_bar)

        self.report_label = QLabel("Waiting for report generation task...")
        self.report_label.setWordWrap(True)
        self.report_label.setStyleSheet("color: #abb2bf; font-style: italic; background-color: #282c34; padding: 10px; border-radius: 4px;")
        right_layout.addWidget(self.report_label)

        main_layout.addWidget(right_widget, stretch=4)

        # Footer Status Bar
        self.health_label = QLabel("Health Check: INITIALIZING...")
        self.health_label.setStyleSheet("color: #e5c07b; font-weight: bold; margin-left: 10px;")
        self.statusBar().addWidget(self.health_label)

    def _connect_signals(self) -> None:
        self.bridge.student_added.connect(self.on_student_added)
        self.bridge.student_updated.connect(self.on_student_updated)
        self.bridge.student_deleted.connect(self.on_student_deleted)
        self.bridge.report_progress.connect(self.on_report_progress)
        self.bridge.report_completed.connect(self.on_report_completed)
        self.bridge.all_events_logged.connect(self.on_all_events_logged)
        self.bridge.health_updated.connect(self.on_health_updated)

    def _load_existing_students(self) -> None:
        students = self.repo.get_all()
        for s in students:
            self._add_or_update_row(s)

    def _add_or_update_row(self, s: Student) -> None:
        # Find if student already exists in the table (by UUID)
        row_idx = -1
        for i in range(self.table.rowCount()):
            if self.table.item(i, 0).text() == s.id:
                row_idx = i
                break

        if row_idx == -1:
            row_idx = self.table.rowCount()
            self.table.insertRow(row_idx)

        # Populate columns
        self.table.setItem(row_idx, 0, QTableWidgetItem(s.id))
        self.table.setItem(row_idx, 1, QTableWidgetItem(s.student_id))
        self.table.setItem(row_idx, 2, QTableWidgetItem(s.full_name))
        self.table.setItem(row_idx, 3, QTableWidgetItem(str(s.age)))
        self.table.setItem(row_idx, 4, QTableWidgetItem(s.gender))
        self.table.setItem(row_idx, 5, QTableWidgetItem(s.major))
        
        gpa_item = QTableWidgetItem(f"{s.gpa:.2f}")
        gpa_item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row_idx, 6, gpa_item)

    @Slot(object)
    def on_student_added(self, student: Student) -> None:
        self._add_or_update_row(student)

    @Slot(object)
    def on_student_updated(self, student: Student) -> None:
        self._add_or_update_row(student)

    @Slot(str)
    def on_student_deleted(self, uuid: str) -> None:
        # Find and remove row
        for i in range(self.table.rowCount()):
            if self.table.item(i, 0).text() == uuid:
                self.table.removeRow(i)
                break

    @Slot(int)
    def on_report_progress(self, progress: int) -> None:
        self.progress_bar.setValue(progress)
        self.report_label.setText(f"Calculating averages... Progress: {progress}%")
        self.report_label.setStyleSheet("color: #e5c07b; font-style: normal; background-color: #282c34; padding: 10px; border-radius: 4px;")

    @Slot(str)
    def on_report_completed(self, report: str) -> None:
        self.progress_bar.setValue(100)
        self.report_label.setText(report)
        self.report_label.setStyleSheet("color: #98c379; font-weight: bold; background-color: #282c34; padding: 10px; border-radius: 4px;")

    @Slot(str, str)
    def on_all_events_logged(self, event_name: str, event_data: str) -> None:
        # Format payload length to look readable in the log
        payload = event_data if len(event_data) <= 60 else event_data[:57] + "..."
        log_text = f"⚡ [EventBus] {event_name}"
        if payload:
            log_text += f" | Data: {payload}"
        self.log_list.insertItem(0, log_text)

    @Slot(object)
    def on_health_updated(self, status: dict) -> None:
        overall = status.get("status", "unknown").upper()
        comps = status.get("components", {})
        details = ", ".join(f"{k.capitalize()}: {v}" for k, v in comps.items())
        
        self.health_label.setText(f"System Health: {overall} ({details})")
        if overall == "HEALTHY":
            self.health_label.setStyleSheet("color: #98c379; font-weight: bold; margin-left: 10px;")
        else:
            self.health_label.setStyleSheet("color: #e06c75; font-weight: bold; margin-left: 10px;")
