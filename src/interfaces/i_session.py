from abc import ABC, abstractmethod
from typing import Any, TypeVar

T = TypeVar("T")


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

    @abstractmethod
    def add(self, entity: Any) -> None:
        """
        @brief Adds an entity to the session.
        """
        ...

    @abstractmethod
    def get(self, entity_class: type[T], entity_id: Any) -> T | None:
        """
        @brief Retrieves an entity by its class and ID.
        """
        ...

    @abstractmethod
    def merge(self, entity: Any) -> Any:
        """
        @brief Merges the state of the given entity into the current session.
        """
        ...

    @abstractmethod
    def delete(self, entity: Any) -> None:
        """
        @brief Deletes an entity from the session.
        """
        ...

    def close(self) -> None:
        """
        @brief Closes the session.
        """
        pass

    def __enter__(self) -> "ISession":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        try:
            if exc_type is not None:
                self.rollback()
        finally:
            self.close()
