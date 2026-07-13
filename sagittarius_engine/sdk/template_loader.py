import os
from typing import List

from sagittarius_engine.exceptions import PathTraversalError


class TemplateLoader:
    """
    @brief Responsible for dynamically discovering and locating templates.
    """

    def __init__(self) -> None:
        self.template_directories: List[str] = [
            os.path.join(os.path.dirname(__file__), "templates")
        ]

    def register_template_directory(self, path: str) -> None:
        """
        @brief Registers an additional directory to search for templates.
        """
        if os.path.exists(path) and os.path.isdir(path):
            self.template_directories.append(path)

    def list_templates(self) -> List[str]:
        """
        @brief Scans template directories dynamically and lists all discovered template names.
        """
        templates = set()
        for directory in self.template_directories:
            if os.path.exists(directory) and os.path.isdir(directory):
                for name in os.listdir(directory):
                    if os.path.isdir(os.path.join(directory, name)):
                        templates.add(name)
        return sorted(list(templates))

    def get_template_path(self, template_name: str) -> str:
        """
        @brief Resolves the absolute directory path of a given template.
        """
        for directory in self.template_directories:
            base_dir_real = os.path.realpath(directory)
            path = os.path.join(directory, template_name)
            full_path_real = os.path.realpath(path)

            if os.path.commonpath([base_dir_real, full_path_real]) != base_dir_real:
                raise PathTraversalError(f"Path traversal detected: {template_name}")

            if os.path.exists(full_path_real) and os.path.isdir(full_path_real):
                return full_path_real
        raise ValueError(f"Template '{template_name}' not found.")
