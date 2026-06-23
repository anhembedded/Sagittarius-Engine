from typing import Any, Callable
from src.core import IMiddleware

class ValidationMiddleware(IMiddleware):
    def process(self, cmd_or_query: Any, dto: Any, next_handler: Callable[[], Any]) -> Any:
        print(f"[ValidationMiddleware] Validating DTO for {cmd_or_query.__class__.__name__}")
        # Demo validation: check if dto is not None if we strictly require it
        if dto is None:
            print("[ValidationMiddleware] Warning: DTO is None!")
        return next_handler()
