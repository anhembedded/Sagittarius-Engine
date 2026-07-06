from abc import ABC, abstractmethod
from typing import Any


class IQuery(ABC):
    """
    @brief Interface for Queries in the CQRS architecture.

    @details A Query is responsible for fetching data from the system WITHOUT changing its state
    (Read-only operations).

    @par Tutorial / Usage Example:
    @code
    class GetUserQuery(IQuery):
        def execute(self, input_dto: GetUserDTO) -> User:
            # Logic to query the database goes here
            pass
    @endcode
    """

    @abstractmethod
    def execute(self, input_dto: Any) -> Any:
        """
        @brief Executes the query.

        @param input_dto The query parameters.
        @return The data retrieved from the system.
        """
        ...
