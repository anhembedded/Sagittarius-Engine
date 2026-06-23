from typing import Any, Callable
from src.core import IMiddleware, ILogger, IContainer

class LoggingMiddleware(IMiddleware):
    def __init__(self, container: IContainer):
        self.container = container

    def process(self, cmd_or_query: Any, dto: Any, next_handler: Callable[[], Any]) -> Any:
        name = cmd_or_query.__class__.__name__

        try:
            logger = self.container.resolve(ILogger)
            logger.info(f"[LoggingMiddleware] Starting {name}")
        except Exception:
            logger = None
            print(f"[LoggingMiddleware] Starting {name}")

        result = next_handler()

        if logger:
            logger.info(f"[LoggingMiddleware] Finished {name}")
        else:
            print(f"[LoggingMiddleware] Finished {name}")

        return result
