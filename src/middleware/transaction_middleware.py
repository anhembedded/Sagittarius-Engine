from collections.abc import Callable
from typing import Any

from src.application.ports import IContainer, IMiddleware
from src.infrastructure.persistence.i_session import ISession


class TransactionMiddleware(IMiddleware):
    """
    @brief Middleware for managing database transactions.

    @details This middleware dynamically resolves an `ISession` from the container,
    wraps the command execution in a transaction, and commits the transaction if the
    command succeeds, or rolls back if an exception occurs.
    """

    def __init__(self, container: IContainer):
        self._container = container

    def process(
        self, cmd_or_query: Any, data_transfer_obj: Any, next_handler: Callable[[], Any]
    ) -> Any:
        session = self._container.resolve(ISession)
        try:
            result = next_handler()
            session.commit()
            return result
        except Exception:
            session.rollback()
            raise
