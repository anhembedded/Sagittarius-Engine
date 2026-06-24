from typing import Any, Callable
from src.interfaces import IMiddleware
import time

class TimingMiddleware(IMiddleware):
    """
    @brief Middleware used to measure the execution time of a Command or Query.

    @par Tutorial / Usage Example:
    @code
    app.use_middleware(TimingMiddleware())

    # The terminal output will show:
    # [TimingMiddleware] ProcessOrderCommand executed in 12.50 ms
    @endcode
    """
    def process(self, cmd_or_query: Any, dto: Any, next_handler: Callable[[], Any]) -> Any:
        """
        @brief Processes the command or query, measuring and printing the execution time.

        @param cmd_or_query The Command or Query instance being executed.
        @param dto The input data.
        @param next_handler The next middleware or the final execution function.
        @return The result of the operation.
        """
        start_time = time.time()
        result = next_handler()
        end_time = time.time()
        duration = (end_time - start_time) * 1000
        print(f"[TimingMiddleware] {cmd_or_query.__class__.__name__} executed in {duration:.2f} ms")
        return result
