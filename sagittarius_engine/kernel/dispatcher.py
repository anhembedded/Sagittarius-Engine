from typing import Any
from sagittarius_engine.interfaces import ICommand, IQuery, ILogger


class Dispatcher:
    """Responsible for executing handlers through the middleware pipeline."""

    def __init__(self, context: Any) -> None:
        self.context = context

    def _get_logger(self) -> ILogger | None:
        return self.context.logger

    def execute(self, command_class: type[ICommand], input_dto: Any = None) -> Any:
        logger = self._get_logger()
        if logger:
            logger.info(f"Executing command: {command_class.__name__}")
        command = self.context.container.resolve(command_class)

        def final() -> Any:
            return command.execute(input_dto)

        return self.context.middleware_pipeline.execute(command, input_dto, final)

    def query(self, query_class: type[IQuery], input_dto: Any = None) -> Any:
        logger = self._get_logger()
        if logger:
            logger.info(f"Executing query: {query_class.__name__}")
        query = self.context.container.resolve(query_class)

        def final() -> Any:
            return query.execute(input_dto)

        return self.context.middleware_pipeline.execute(query, input_dto, final)
