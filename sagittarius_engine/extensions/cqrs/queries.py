from abc import ABC, abstractmethod
from typing import Any


class IQuery(ABC):
    """
    @brief Interface for Queries in the CQRS architecture.

    @details A Query is responsible for fetching data from the system WITHOUT changing its state
    (Read-only operations).
    """

    @abstractmethod
    def execute(self, input_dto: Any) -> Any:
        """
        @brief Executes the query.
        @param input_dto The query parameters.
        @return The data retrieved from the system.
        """
        ...
