from typing import Any, Callable
from src.core import IMiddleware
import time

class LoggingMiddleware(IMiddleware):
    def process(self, cmd_or_query: Any, dto: Any, next_handler: Callable[[], Any]) -> Any:
        name = cmd_or_query.__class__.__name__
        print(f"[LoggingMiddleware] Starting {name}")
        result = next_handler()
        print(f"[LoggingMiddleware] Finished {name}")
        return result
