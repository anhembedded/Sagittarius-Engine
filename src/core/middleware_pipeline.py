from collections.abc import Callable
from functools import partial
from typing import Any
from src.interfaces import IMiddleware

class MiddlewarePipeline:
    """
    Manages a chain of Middlewares using the Onion execution pattern:
    - Requests flow inward through each middleware until they reach the core handler.
    - Results flow outward back through the middleware chain.
    """

    def __init__(self) -> None:
        self.middlewares: list[IMiddleware] = []

    def add(self, middleware: IMiddleware) -> None:
        """Append a middleware to the end of the chain."""
        self.middlewares.append(middleware)

    def execute(self, cmd_or_query: Any, dto: Any, final_handler: Callable[[], Any]) -> Any:
        """
        Execute the entire middleware chain.

        Args:
            cmd_or_query: The Command or Query instance.
            dto: The Data Transfer Object input.
            final_handler: The final execution handler for the Command/Query.

        Returns:
            The final execution result after passing through the pipeline.
        """
        handler = final_handler
        for middleware in reversed(self.middlewares):
            handler = partial(middleware.process, cmd_or_query, dto, handler)
        return handler()
