from typing import Any, TypeVar

TResult_co = TypeVar("TResult_co", covariant=True)


class IDispatchable:
    """
    @brief Marker Protocol for handlers that can be dispatched via App.dispatch().

    @details Any handler class that implements `execute(dto: Any) -> TResult`
    is considered dispatchable. Both ICommand and IQuery extend this interface,
    allowing App.dispatch() to infer the return type from the handler type.

    Usage:
        # Mypy infers result: bool
        result = app.dispatch(CreateUserHandler, dto)
    """

    def execute(self, dto: Any) -> Any:
        """@brief Execute the handler with the given DTO."""
        ...
