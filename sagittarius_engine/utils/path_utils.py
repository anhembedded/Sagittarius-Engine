import os


class PathUtils:
    """
    @brief Utilities for working with file paths cleanly.
    """

    @staticmethod
    def get_relative_path(base_file: str, *paths: str) -> str:
        """
        @brief Resolves a path relative to the directory of the given base_file.

        @param base_file The __file__ of the caller.
        @param paths The relative path segments to join.
        @return The absolute path.
        """
        return os.path.join(os.path.dirname(os.path.abspath(base_file)), *paths)
