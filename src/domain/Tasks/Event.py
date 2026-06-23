from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

class DomainEvent(ABC):
    """Base cho mọi domain event."""
    def __init__(self, event_id: Optional[str] = None, occurred_at: Optional[datetime] = None):
        self.event_id = event_id or str(datetime.now().timestamp())  # đơn giản
        self.occurred_at = occurred_at or datetime.now()


@dataclass
class FileOpenedEvent(DomainEvent):
    """Event phát ra khi một file được mở thành công hoặc thất bại."""
    file_path: str
    success: bool
    message: str
    def __init__(self, file_path: str, success: bool, message: str = "",
                 event_id: Optional[str] = None, occurred_at: Optional[datetime] = None):
        super().__init__(event_id, occurred_at)
        self.file_path = file_path
        self.success = success
        self.message = message


@dataclass
class RunnableFilesListedEvent(DomainEvent):
    """Event chứa danh sách các file khả thi được tìm thấy."""
    folder_path: str
    files_count: int
    def __init__(self, folder_path: str, files_count: int,
                 event_id: Optional[str] = None, occurred_at: Optional[datetime] = None):
        super().__init__(event_id, occurred_at)
        self.folder_path = folder_path
        self.files_count = files_count


@dataclass
class TaskProgressEvent(DomainEvent):
    """Event báo cáo tiến độ thực thi của một Task bất kỳ."""
    task_name: str
    percent: float
    message: str
    def __init__(self, task_name: str, percent: float, message: str,
                 event_id: Optional[str] = None, occurred_at: Optional[datetime] = None):
        super().__init__(event_id, occurred_at)
        self.task_name = task_name
        self.percent = percent
        self.message = message