from typing import Any, Type

from src.app_kernel import App
from src.interfaces.i_command import ICommand
from src.interfaces.i_input_port import IInputPort
from src.interfaces.i_output_port import IOutputPort
from src.interfaces.i_query import IQuery

COMMAND_KEY = "command"
EXIT_COMMAND = "exit"


class ApplicationRunner:
    """
    @brief ApplicationRunner orchestrates the execution of an application core via ports.
    """

    def __init__(
        self, app: App, input_port: IInputPort, output_port: IOutputPort
    ) -> None:
        self.app = app
        self.input_port = input_port
        self.output_port = output_port

    def run_cli_loop(
        self,
        command_map: dict[str, Type[ICommand]],
        query_map: dict[str, Type[IQuery]],
    ) -> None:
        """
        @brief Runs a continuous loop receiving input, matching commands/queries, executing them, and presenting output.
        """
        while True:
            try:
                input_data = self.input_port.receive()
                command_name = input_data.get(COMMAND_KEY)

                if command_name == EXIT_COMMAND:
                    break

                if command_name in command_map:
                    cmd_cls = command_map[command_name]
                    result = self.execute(cmd_cls, input_data)
                    self.output_port.present(result)
                elif command_name in query_map:
                    query_cls = query_map[command_name]
                    result = self.query(query_cls, input_data)
                    self.output_port.present(result)
                else:
                    self.output_port.present_error(
                        ValueError(f"Unknown command: {command_name}")
                    )

            except KeyboardInterrupt:
                break
            except Exception as e:
                self.output_port.present_error(e)

    def execute(self, command_class: Type[ICommand], dto: Any = None) -> Any:
        """
        @brief Convenience method for executing a command via the app.
        """
        return self.app.execute(command_class, dto)

    def query(self, query_class: Type[IQuery], dto: Any = None) -> Any:
        """
        @brief Convenience method for executing a query via the app.
        """
        return self.app.query(query_class, dto)
