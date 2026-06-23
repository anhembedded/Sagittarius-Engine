from typing import Any, Callable
from src.core import IMiddleware
import time

class TimingMiddleware(IMiddleware):
    def process(self, cmd_or_query: Any, dto: Any, next_handler: Callable[[], Any]) -> Any:
        start_time = time.time()
        result = next_handler()
        end_time = time.time()
        duration = (end_time - start_time) * 1000
        print(f"[TimingMiddleware] {cmd_or_query.__class__.__name__} executed in {duration:.2f} ms")
        return result
