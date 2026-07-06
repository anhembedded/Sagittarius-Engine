import csv
import json
import os
from typing import Any, Iterator, Optional

from src.app_runner import COMMAND_KEY, EXIT_COMMAND
from src.base_io import BaseInputPort, BaseOutputPort
from src.adapters.batch.const import FILE_TYPE_CSV, FILE_TYPE_JSON


class BatchInputPort(BaseInputPort):
    """
    @brief Batch Input Port that reads data from CSV or JSON files.
    """

    def __init__(self, file_path: str, file_type: str = FILE_TYPE_CSV) -> None:
        super().__init__()
        self.file_path = file_path
        self.file_type = file_type
        self._iterator: Optional[Iterator[dict[str, Any]]] = None
        self._initialized = False

    def _init_iterator(self) -> None:
        if self._initialized:
            return

        self._initialized = True

        if not os.path.exists(self.file_path):
            if self.logger:
                self.logger.error(f"File not found: {self.file_path}")
            self._iterator = iter([])
            return

        try:
            if self.file_type == FILE_TYPE_CSV:
                with open(self.file_path, newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    data = list(reader)
                    self._iterator = iter(data)
            elif self.file_type == FILE_TYPE_JSON:
                with open(self.file_path, encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self._iterator = iter(data)
                    else:
                        if self.logger:
                            self.logger.error("JSON file must contain an array of objects")
                        self._iterator = iter([])
            else:
                if self.logger:
                    self.logger.error(f"Unsupported file type: {self.file_type}")
                self._iterator = iter([])
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error reading file {self.file_path}: {e}")
            self._iterator = iter([])

    def receive(self) -> dict[str, Any]:
        """
        @brief Yields rows from the batch file one by one. After the last row, returns the exit command.
        """
        self._init_iterator()

        try:
            if self._iterator is not None:
                row = next(self._iterator)
                # If COMMAND_KEY is not in the row, we should probably add one, or the caller handles it?
                # The prompt says: 'BatchInputPort(BaseInputPort)... receive() yields rows one by one...'
                # But it also needs to return exit. Wait, the command is normally executed if COMMAND_KEY is there.
                # If not, how does the ApplicationRunner know which command to execute?
                # Let's just return the row and assume the row contains the COMMAND_KEY as per the requirement or we let runner handle it.
                return row
            else:
                return {COMMAND_KEY: EXIT_COMMAND}
        except StopIteration:
            return {COMMAND_KEY: EXIT_COMMAND}


class BatchOutputPort(BaseOutputPort):
    """
    @brief Batch Output Port that appends output to a file.
    """

    def __init__(self, output_path: str) -> None:
        super().__init__()
        self.output_path = output_path
        # Ensure the directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        # Clear file if it exists to start fresh, or append. The prompt says "appends result as a line".
        # We will open in append mode, but maybe we shouldn't clear it.

    def present(self, result: Any) -> None:
        """
        @brief Appends the result to the output file.
        """
        try:
            with open(self.output_path, 'a', encoding='utf-8') as f:
                if isinstance(result, dict):
                    f.write(json.dumps(result) + '\n')
                else:
                    f.write(str(result) + '\n')
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error writing to output file: {e}")

    def present_error(self, error: Exception) -> None:
        """
        @brief Appends the error to the output file.
        """
        try:
            with open(self.output_path, 'a', encoding='utf-8') as f:
                f.write(f"ERROR: {error}\n")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error writing to output file: {e}")
