from abc import ABC, abstractmethod
from typing import Any


class ISession(ABC):
    """
    @brief Interface for Database Session.

    @details Provides an abstraction over database ORMs or connections.
    """

    @abstractmethod
    def commit(self) -> None:
        """@brief Commits the current transaction."""
        ...

    @abstractmethod
    def rollback(self) -> None:
        """@brief Rolls back the current transaction."""
        ...

    @abstractmethod
    def execute(self, statement: Any, params: Any = None) -> Any:
        """
        @brief Executes a raw statement or query.

        @param statement The query or statement to execute.
        @param params Optional parameters for the query.
        @return The result of the execution.
        """
        ...

    @abstractmethod
    def query(self, *entities: Any) -> Any:
        """
        @brief Queries the database for the given entities.

        @param entities The entities (e.g. models or columns) to query.
        @return A query object.
        """
        ...
