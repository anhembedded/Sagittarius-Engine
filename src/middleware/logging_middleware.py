from collections.abc import Callable
from typing import Any

from src.application.ports import IContainer, ILogger, IMiddleware


class LoggingMiddleware(IMiddleware):
    """
    @brief Middleware used to automatically log before and after executing a Command/Query.

    @details It automatically resolves `ILogger` from the Container. If there is an error retrieving
    the logger, it falls back to using the basic `print` command.

    @par Tutorial / Usage Example:
    @code
    app.use_middleware(LoggingMiddleware(container))

    # When app.execute(MyCommand) is called, the following logs will be printed:
    # [LoggingMiddleware] Starting MyCommand
    # ... executes MyCommand logic ...
    # [LoggingMiddleware] Finished MyCommand
    @endcode
    """

    def __init__(self, container: IContainer):
        """
        @brief Constructor.
        @param container The dependency injection container used to resolve the logger.
        """
        self.container = container

    def process(
        self, cmd_or_query: Any, data_transfer_obj: Any, next_handler: Callable[[], Any]
    ) -> Any:
        """
        @brief Processes the command or query, adding logging before and after.

        @param cmd_or_query The Command or Query instance being executed.
        @param data_transfer_obj The input data.
        @param next_handler The next middleware or the final execution function.
        @return The result of the operation.
        """
        name = cmd_or_query.__class__.__name__

        try:
            logger: ILogger = self.container.resolve(ILogger)
            logger.info(f"[LoggingMiddleware] Starting {name}")
        except Exception:
            logger = None  # type: ignore[assignment]
            print(f"[LoggingMiddleware] Starting {name}")

        result = next_handler()

        if logger:
            logger.info(f"[LoggingMiddleware] Finished {name}")
        else:
            print(f"[LoggingMiddleware] Finished {name}")

        return result
