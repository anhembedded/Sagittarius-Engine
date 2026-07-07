import sys
from pprint import pprint
from typing import Any
from src.core.base_output_port import BaseOutputPort

class CLIOutputPort(BaseOutputPort):
    """
    @brief CLI Output Port that prints results to stdout and errors to stderr.
    """

    def present(self, result: Any) -> None:
        """
        @brief Pretty prints the result to stdout.
        """
        if result is not None:
            pprint(result)

    def present_error(self, error: Exception) -> None:
        """
        @brief Prints the error to stderr.
        """
        print(f'ERROR: {error}', file=sys.stderr)
