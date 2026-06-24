from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, Union, Optional

class ICommand(ABC):
    """
    @brief Interface for Commands in the CQRS architecture.

    @details A Command is responsible for executing operations that change the system's state
    (Write operations), such as Create, Update, or Delete.

    @par Tutorial / Usage Example:
    @code
    class CreateUserCommand(ICommand):
        def execute(self, input_dto: CreateUserDTO) -> User:
            # Logic to save user to the database goes here
            pass
    @endcode
    """

    @abstractmethod
    def execute(self, input_dto: Any) -> Any:
        """
        @brief Executes the command.

        @param input_dto The input Data Transfer Object to be processed.
        @return The execution result (if any).
        """
        ...
