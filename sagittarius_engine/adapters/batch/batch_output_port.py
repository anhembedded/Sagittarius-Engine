import json
import os
from typing import Any
from sagittarius_engine.base.base_output_port import BaseOutputPort
from sagittarius_engine.exceptions import PathTraversalError


class BatchOutputPort(BaseOutputPort):
    """
    @brief Batch Output Port that appends output to a file.
    """

    def __init__(self, output_path: str, allowed_dir: str = ".") -> None:
        super().__init__()

        # Path traversal prevention
        allowed_real = os.path.realpath(allowed_dir)
        full_path_real = os.path.realpath(os.path.join(allowed_real, output_path))

        if os.path.commonpath([allowed_real, full_path_real]) != allowed_real:
            raise PathTraversalError(f"Path traversal detected: {output_path}")

        self.output_path = full_path_real
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

    def present(self, result: Any) -> None:
        """
        @brief Appends the result to the output file.
        """
        try:
            with open(self.output_path, "a", encoding="utf-8") as f:
                if isinstance(result, dict):
                    f.write(json.dumps(result) + "\n")
                else:
                    f.write(str(result) + "\n")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error writing to output file: {e}")

    def present_error(self, error: Exception) -> None:
        """
        @brief Appends the error to the output file.
        """
        try:
            with open(self.output_path, "a", encoding="utf-8") as f:
                f.write(f"ERROR: {error}\n")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error writing to output file: {e}")
