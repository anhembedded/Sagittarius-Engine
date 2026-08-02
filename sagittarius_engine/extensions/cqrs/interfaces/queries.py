from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

TInput = TypeVar("TInput", bound=Any)
TOutput = TypeVar("TOutput", bound=Any)


class IQuery(Generic[TInput, TOutput], ABC):
    """
    @brief Interface for Queries in the CQRS architecture.

    @details A Query is responsible for fetching data from the system WITHOUT changing its state
    (Read-only operations).
    """

    @abstractmethod
    def execute(self, input_dto: TInput) -> TOutput:
        """
        @brief Executes the query.
        @param input_dto The query parameters.
        @return The data retrieved from the system.
        """
        ...
