from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any


class IMiddleware(ABC):
    """
    @brief Interface for Middleware.

    @details Middleware acts as filters that run before and after the execution of
    a Command or Query. Highly useful for Logging, Validation, Authorization.

    @par Tutorial / Usage Example:
    @code
    class MyMiddleware(IMiddleware):
        def process(self, cmd_or_query, data_transfer_obj, next_handler):
            print("Before executing the command")
            result = next_handler()  # Calls the next handler or the main command
            print("After executing the command")
            return result
    @endcode
    """

    @abstractmethod
    def process(
        self, cmd_or_query: Any, data_transfer_obj: Any, next_handler: Callable[[], Any]
    ) -> Any:
        """
        @brief Processes the command or query.

        @param cmd_or_query The Command or Query instance being executed.
        @param data_transfer_obj The Data Transfer Object input.
        @param next_handler The next middleware or the final execution function.
        @return The result of the operation.
        """
        ...
