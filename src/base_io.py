from typing import Any, Optional

from src.interfaces.i_input_port import IInputPort
from src.interfaces.i_logger import ILogger
from src.interfaces.i_output_port import IOutputPort


class BaseInputPort(IInputPort):
    """
    @brief Base class for input ports.
    """

    def __init__(self, logger: Optional[ILogger] = None) -> None:
        self.logger = logger

    def receive(self) -> dict[str, Any]:
        """
        @brief Receives input. To be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement receive()")


class BaseOutputPort(IOutputPort):
    """
    @brief Base class for output ports.
    """

    def __init__(self, logger: Optional[ILogger] = None) -> None:
        self.logger = logger

    def present(self, result: Any) -> None:
        """
        @brief Presents the result. Logs if logger exists, else prints.
        """
        if self.logger:
            self.logger.info(f"Result: {result}")
        else:
            print(result)

    def present_error(self, error: Exception) -> None:
        """
        @brief Presents the error. Logs if logger exists, else prints.
        """
        if self.logger:
            self.logger.error(f"Error: {error}")
        else:
            print(f"Error: {error}")
