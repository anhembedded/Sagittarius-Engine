from typing import Any, Callable
from src.core import IMiddleware

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
    def process(self, cmd_or_query: Any, dto: Any, next_handler: Callable[[], Any]) -> Any:
        """
        @brief Processes the command or query, validating the input DTO.

        @param cmd_or_query The Command or Query instance being executed.
        @param dto The input data to validate.
        @param next_handler The next middleware or the final execution function.
        @return The result of the operation.
        """
        print(f"[ValidationMiddleware] Validating DTO for {cmd_or_query.__class__.__name__}")
        if dto is None:
            print("[ValidationMiddleware] Warning: DTO is None!")
        return next_handler()
