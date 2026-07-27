# Clean Architecture - MVP Passive View Implementation
from typing import Any, Sequence
import sys
from PySide6.QtCore import Slot, Qt
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
from examples.student_management.application.contracts.student_monitor_view import IStudentMonitorView
from examples.student_management.domain.student import Student
from examples.student_management.presentation.ui.event_bridge import EventBridge
from examples.student_management.presentation.presenters.student_monitor_presenter import StudentMonitorPresenter


class MainWindow(QMainWindow, IStudentMonitorView):
    """
    # MVP Pattern - View Implementation
    Passive View implementing IStudentMonitorView.
    Responsible strictly for PySide6 Qt layout, widgets creation, and styling.
    All presentation/business logic is delegated to StudentMonitorPresenter.
    """

    def __init__(self, app: App, bridge: EventBridge) -> None:
        super().__init__()
        self.app = app
        self.bridge = bridge

        self.setWindowTitle("Sagittarius Engine - Student Monitor (PySide6 Clean Architecture)")
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
        self.presenter = StudentMonitorPresenter(self, app)
        self._connect_signals()
        self.presenter.initialize()

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
        table_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        table_title.setStyleSheet("color: #61afef; margin-bottom: 5px;")
        left_layout.addWidget(table_title)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["Internal UUID", "Student ID", "Full Name", "Age", "Gender", "Major", "GPA"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        left_layout.addWidget(left_widget, stretch=7)

        # --- RIGHT PANEL: Real-time Monitor Logs & Progress ---
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(12)

        # Log Header
        log_title = QLabel("⚡ UNIVERSAL EVENT BUS LOGS")
        log_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        log_title.setStyleSheet("color: #61afef;")
        right_layout.addWidget(log_title)

        self.log_list = QListWidget()
        right_layout.addWidget(self.log_list)

        # Progress Header
        progress_title = QLabel("📊 GPA ANALYTICS REPORT (ASYNC)")
        progress_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        progress_title.setStyleSheet("color: #e5c07b;")
        right_layout.addWidget(progress_title)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        right_layout.addWidget(self.progress_bar)

        self.report_label = QLabel("Waiting for report generation task...")
        self.report_label.setWordWrap(True)
        self.report_label.setStyleSheet("color: #abb2bf; font-style: italic; background-color: #282c34; padding: 10px; border-radius: 4px;")
        right_layout.addWidget(right_widget, stretch=4)

        # Footer Status Bar
        self.health_label = QLabel("Health Check: INITIALIZING...")
        self.health_label.setStyleSheet("color: #e5c07b; font-weight: bold; margin-left: 10px;")
        self.statusBar().addWidget(self.health_label)

    def _connect_signals(self) -> None:
        self.bridge.student_added.connect(self.presenter.on_student_added)
        self.bridge.student_updated.connect(self.presenter.on_student_updated)
        self.bridge.student_deleted.connect(self.presenter.on_student_deleted)
        self.bridge.report_progress.connect(self.presenter.on_report_progress)
        self.bridge.report_completed.connect(self.presenter.on_report_completed)
        self.bridge.all_events_logged.connect(self.presenter.on_event_logged)
        self.bridge.health_updated.connect(self.presenter.on_health_updated)

    # --- IStudentMonitorView Passive View Contract Methods ---

    def display_students(self, students: Sequence[Student]) -> None:
        self.table.setRowCount(0)
        for s in students:
            self.update_student_row(s)

    def update_student_row(self, s: Student) -> None:
        row_idx = -1
        for i in range(self.table.rowCount()):
            item = self.table.item(i, 0)
            if item is not None and item.text() == s.id:
                row_idx = i
                break

        if row_idx == -1:
            row_idx = self.table.rowCount()
            self.table.insertRow(row_idx)

        self.table.setItem(row_idx, 0, QTableWidgetItem(s.id))
        self.table.setItem(row_idx, 1, QTableWidgetItem(s.student_id))
        self.table.setItem(row_idx, 2, QTableWidgetItem(s.full_name))
        self.table.setItem(row_idx, 3, QTableWidgetItem(str(s.age)))
        self.table.setItem(row_idx, 4, QTableWidgetItem(s.gender))
        self.table.setItem(row_idx, 5, QTableWidgetItem(s.major))
        
        gpa_item = QTableWidgetItem(f"{s.gpa:.2f}")
        gpa_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setItem(row_idx, 6, gpa_item)

    def remove_student_row(self, uuid: str) -> None:
        for i in range(self.table.rowCount()):
            item = self.table.item(i, 0)
            if item is not None and item.text() == uuid:
                self.table.removeRow(i)
                break

    def update_report_progress(self, progress: int) -> None:
        self.progress_bar.setValue(progress)
        self.report_label.setText(f"Calculating averages... Progress: {progress}%")
        self.report_label.setStyleSheet("color: #e5c07b; font-style: normal; background-color: #282c34; padding: 10px; border-radius: 4px;")

    def display_report(self, report_text: str) -> None:
        self.progress_bar.setValue(100)
        self.report_label.setText(report_text)
        self.report_label.setStyleSheet("color: #98c379; font-weight: bold; background-color: #282c34; padding: 10px; border-radius: 4px;")

    def add_event_log(self, event_name: str, event_data: str) -> None:
        payload = event_data if len(event_data) <= 60 else event_data[:57] + "..."
        log_text = f"⚡ [EventBus] {event_name}"
        if payload:
            log_text += f" | Data: {payload}"
        self.log_list.insertItem(0, log_text)

    def update_health_status(self, status: dict[str, Any]) -> None:
        overall = status.get("status", "unknown").upper()
        comps = status.get("components", {})
        details = ", ".join(f"{k.capitalize()}: {v}" for k, v in comps.items())
        
        self.health_label.setText(f"System Health: {overall} ({details})")
        if overall == "HEALTHY":
            self.health_label.setStyleSheet("color: #98c379; font-weight: bold; margin-left: 10px;")
        else:
            self.health_label.setStyleSheet("color: #e06c75; font-weight: bold; margin-left: 10px;")
