from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sagittarius_engine.interfaces.i_dispatchable import IDispatchable

TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")


class IQuery(Generic[TInput, TOutput], IDispatchable, ABC):
    """
    @brief Interface for Queries in the CQRS architecture.

    @details A Query is responsible for fetching data from the system WITHOUT changing its state
    (Read-only operations).

    Generic parameters:
        TInput: The DTO type accepted by execute().
        TOutput: The data type returned by execute().
    """

    @abstractmethod
    def execute(self, input_dto: TInput) -> TOutput:  # type: ignore[override]
        """
        @brief Executes the query.
        @param input_dto The query parameters.
        @return The data retrieved from the system.
        """
        ...
