from typing import Any, Optional
from sagittarius_engine.interfaces.i_logger import ILogger
from sagittarius_engine.interfaces.i_output_port import IOutputPort

class BaseOutputPort(IOutputPort):
    """
    @brief Base class for output ports.
    """

    def __init__(self, logger: Optional[ILogger]=None) -> None:
        self.logger = logger

    def present(self, result: Any) -> None:
        """
        @brief Presents the result. Logs if logger exists, else prints.
        """
        if self.logger:
            self.logger.info(f'Result: {result}')
        else:
            print(result)

    def present_error(self, error: Exception) -> None:
        """
        @brief Presents the error. Logs if logger exists, else prints.
        """
        if self.logger:
            self.logger.error(f'Error: {error}')
        else:
            import logging
            logging.error(f"BaseOutputPort Error: {error}")
            # 🛡️ Sentinel: Security Concern - Prevent information disclosure by not writing raw exceptions to standard out
            print('Error: An internal error occurred.')
