from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

TInput = TypeVar("TInput", bound=Any)
TOutput = TypeVar("TOutput", bound=Any)


class ICommand(Generic[TInput, TOutput], ABC):
    """
    @brief Interface for Commands in the CQRS architecture.

    @details A Command is responsible for executing operations that change the system's state
    (Write operations), such as Create, Update, or Delete.
    """

    @abstractmethod
    def execute(self, input_dto: TInput) -> TOutput:
        """
        @brief Executes the command.
        @param input_dto The input Data Transfer Object to be processed.
        @return The execution result (if any).
        """
        ...
