from collections.abc import Callable
from typing import Any
from src.application.ports import IMiddleware

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
        return self.__build_chain(cmd_or_query, dto, final_handler, 0)()

    def __build_chain(self, cmd_or_query: Any, dto: Any, final_handler: Callable[[], Any], index: int) -> Callable[[], Any]:
        """
        Private helper method to recursively build the middleware chain.
        Each middleware wraps around the next one until the final handler.
        """
        if index >= len(self.middlewares):
            return final_handler
        middleware = self.middlewares[index]
        return lambda: self.__invoke_middleware(middleware, cmd_or_query, dto, final_handler, index)

    def __invoke_middleware(self, middleware: IMiddleware, cmd_or_query: Any, dto: Any, final_handler: Callable[[], Any], index: int) -> Any:
        """
        Invoke a single middleware and pass control to the next one.
        """
        return middleware.process(cmd_or_query, dto, self.__build_chain(cmd_or_query, dto, final_handler, index + 1))
