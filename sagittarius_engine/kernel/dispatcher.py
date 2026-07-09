from typing import Any
from sagittarius_engine.interfaces import ICommand, IQuery, ILogger

class Dispatcher:
    """Responsible for executing handlers through the middleware pipeline."""

    def __init__(self, app: Any) -> None:
        self.app = app

    def _get_logger(self) -> ILogger | None:
        try:
            from sagittarius_engine.interfaces import ILogger
            return self.app.container.resolve(ILogger)
        except Exception:
            return None

    def execute(self, command_class: type[ICommand], input_dto: Any = None) -> Any:
        logger = self._get_logger()
        if logger:
            logger.info(f"Executing command: {command_class.__name__}")
        command = self.app.container.resolve(command_class)

        def final() -> Any:
            return command.execute(input_dto)

        return self.app.pipeline.execute(command, input_dto, final)

    def query(self, query_class: type[IQuery], input_dto: Any = None) -> Any:
        logger = self._get_logger()
        if logger:
            logger.info(f"Executing query: {query_class.__name__}")
        query = self.app.container.resolve(query_class)

        def final() -> Any:
            return query.execute(input_dto)

        return self.app.pipeline.execute(query, input_dto, final)
