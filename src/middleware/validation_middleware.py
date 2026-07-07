import logging
from collections.abc import Callable
from typing import Any

from src.application.ports import IMiddleware

logger = logging.getLogger(__name__)


class ValidationMiddleware(IMiddleware):
    """
    @brief Middleware used to check the validity (Validate) of the input DTO.

    @details This is a basic example. In a real-world application, you can integrate libraries
    like Pydantic or Marshmallow here to validate the DTO before yielding control
    to the Command execution.

    @par Tutorial / Usage Example:
    @code
    app.use_middleware(ValidationMiddleware())

    # If app.execute(MyCommand, input_dto=None) is called, the Middleware will issue a warning.
    @endcode
    """

    def process(
        self, cmd_or_query: Any, data_transfer_obj: Any, next_handler: Callable[[], Any]
    ) -> Any:
        """
        @brief Processes the command or query, validating the input DTO.

        @param cmd_or_query The Command or Query instance being executed.
        @param data_transfer_obj The input data to validate.
        @param next_handler The next middleware or the final execution function.
        @return The result of the operation.
        """
        logger.debug(
            f"[ValidationMiddleware] Validating DTO for {cmd_or_query.__class__.__name__}"
        )
        if data_transfer_obj is None:
            logger.warning("[ValidationMiddleware] Warning: DTO is None!")
        return next_handler()
