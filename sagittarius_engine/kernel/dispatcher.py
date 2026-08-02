from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from sagittarius_engine.kernel.i_kernel_context import IKernelContext
import warnings
from sagittarius_engine.interfaces import ILogger


class Dispatcher:
    """Responsible for executing handlers through the middleware pipeline."""

    def __init__(self, context: "IKernelContext") -> None:
        self.context = context

    def _get_logger(self) -> ILogger | None:
        return self.context.logger

    def dispatch(
        self,
        handler_class: type,
        input_dto: object | None = None,
    ) -> Any:
        """
        @brief Dispatches a handler (command, query, etc.) through the middleware pipeline.
        """
        logger = self._get_logger()
        if logger:
            msg_type = "query" if "Query" in handler_class.__name__ else "command"
            logger.info(
                f"Executing {msg_type}: {handler_class.__name__}",
                extra={"submodule": "Dispatcher"},
            )
        handler = self.context.container.resolve(handler_class)

        def final() -> Any:
            return handler.execute(input_dto)

        return self.context.middleware_pipeline.execute(handler, input_dto, final)

    def execute(self, command_class: type, input_dto: object | None = None) -> Any:
        """
        @brief Deprecated. Use dispatch instead.
        """
        warnings.warn(
            "Dispatcher.execute is deprecated. Use Dispatcher.dispatch instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.dispatch(command_class, input_dto)

    def query(self, query_class: type, input_dto: object | None = None) -> Any:
        """
        @brief Deprecated. Use dispatch instead.
        """
        warnings.warn(
            "Dispatcher.query is deprecated. Use Dispatcher.dispatch instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.dispatch(query_class, input_dto)
