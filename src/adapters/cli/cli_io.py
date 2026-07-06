import argparse
import sys
from pprint import pprint
from typing import Any

from src.base_io import BaseInputPort, BaseOutputPort
from src.adapters.cli.const import COMMAND_KEY


class CLIInputPort(BaseInputPort):
    """
    @brief CLI Input Port that uses argparse to parse command-line arguments.
    """

    def receive(self) -> dict[str, Any]:
        """
        @brief Parses CLI arguments into a dictionary.

        @return A dictionary containing the command and any parsed arguments.
        """
        parser = argparse.ArgumentParser(description="CLI Input Port")
        parser.add_argument(COMMAND_KEY, type=str, help="The command to execute")

        args, unknown = parser.parse_known_args()

        result = {COMMAND_KEY: getattr(args, COMMAND_KEY)}

        # Parse remaining --key value pairs
        i = 0
        while i < len(unknown):
            arg = unknown[i]
            if arg.startswith("--"):
                key = arg[2:]
                value = None
                if i + 1 < len(unknown) and not unknown[i + 1].startswith("--"):
                    value = unknown[i + 1]
                    i += 1
                result[key] = value
            else:
                # If there are unknown positional arguments, exit or error
                sys.exit(f"error: unrecognized arguments: {arg}")
            i += 1

        return result


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
        print(f"ERROR: {error}", file=sys.stderr)
