from typing import Any, List
from Domain.Tasks.Event import DomainEvent


class Result:
    """Kết quả của một use case. Domain events được trả về để AppController publish."""
    def __init__(self, success: bool, data: Any = None, 
                 error_message: str | None = None, events: list[DomainEvent] | None = None):
        self.success = success
        self.data = data          # dữ liệu trả về (entity, list, file path, ...)
        self.error_message = error_message
        self.events = events or []

    @staticmethod
    def ok(data: Any = None, events: list[DomainEvent] | None = None) -> 'Result':
        return Result(True, data=data, events=events)

    @staticmethod
    def fail(message: str, events: list[DomainEvent] | None = None) -> 'Result':
        return Result(False, error_message=message, events=events)