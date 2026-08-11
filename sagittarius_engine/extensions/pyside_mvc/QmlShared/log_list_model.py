from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt, Signal, Slot
from PySide6.QtGui import QGuiApplication

#: Log level -> the icon name LogPanel.qml renders beside the line, resolved
#: through whatever `image://<scheme>/...` provider the app registered.
#: Unknown levels fall back to "info".
LEVEL_ICONS = {
    "info": "info",
    "error": "triangle-alert",
    "success": "circle-check-big",
}
_DEFAULT_LEVEL = "info"

#: Keeps memory bounded during long-running sessions (e.g. a live-stream
#: monitor) — a model backing a ListView should not grow without limit.
MAX_ENTRIES = 500


@dataclass(frozen=True)
class LogEntry:
    timestamp: str
    message: str
    level: str

    @property
    def icon(self) -> str:
        return LEVEL_ICONS.get(self.level, LEVEL_ICONS[_DEFAULT_LEVEL])


class LogListModel(QAbstractListModel):
    """
    @brief Backs LogPanel.qml — a timestamped, leveled message list shared by
    every screen that shows a log.
    """

    MessageRole = Qt.ItemDataRole.UserRole + 1
    TimestampRole = Qt.ItemDataRole.UserRole + 2
    LevelRole = Qt.ItemDataRole.UserRole + 3
    IconRole = Qt.ItemDataRole.UserRole + 4

    _ROLE_NAMES = {
        MessageRole: b"message",
        TimestampRole: b"timestamp",
        LevelRole: b"level",
        IconRole: b"icon",
    }

    countChanged = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._entries: list[LogEntry] = []

    def rowCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._entries)

    def roleNames(self) -> dict:
        return dict(self._ROLE_NAMES)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not 0 <= index.row() < len(self._entries):
            return None

        entry = self._entries[index.row()]
        if role == self.MessageRole:
            return entry.message
        if role == self.TimestampRole:
            return entry.timestamp
        if role == self.LevelRole:
            return entry.level
        if role == self.IconRole:
            return entry.icon
        return None

    def append(self, message: str, level: str = _DEFAULT_LEVEL) -> None:
        """Appends one line, trimming the oldest once MAX_ENTRIES is reached."""
        if len(self._entries) >= MAX_ENTRIES:
            self.beginRemoveRows(QModelIndex(), 0, 0)
            self._entries.pop(0)
            self.endRemoveRows()

        position = len(self._entries)
        self.beginInsertRows(QModelIndex(), position, position)
        self._entries.append(
            LogEntry(
                timestamp=datetime.now().strftime("%H:%M:%S"),
                message=message,
                level=level,
            )
        )
        self.endInsertRows()
        self.countChanged.emit()

    @Slot()
    def clear(self) -> None:
        """Callable from QML — the panel's own Clear button needs no
        Presenter round-trip."""
        self.beginResetModel()
        self._entries.clear()
        self.endResetModel()
        self.countChanged.emit()

    @Slot()
    def copyAllToClipboard(self) -> None:
        """Callable from QML — the panel's own Copy button needs no
        Presenter round-trip, same as clear() above. Copies every line as
        plain text ("[HH:MM:SS] message", one per line, oldest first —
        matching render order) rather than requiring the user to select text
        across every ListView delegate by hand."""
        text = "\n".join(f"[{entry.timestamp}] {entry.message}" for entry in self._entries)
        QGuiApplication.clipboard().setText(text)

    @property
    def entries(self) -> list[LogEntry]:
        return list(self._entries)
