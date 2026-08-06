import os
import shutil
from sagittarius_engine.sdk.template_loader import TemplateLoader
from sagittarius_engine.sdk.template_renderer import TemplateRenderer
from sagittarius_engine.exceptions import PathTraversalError


class ProjectGenerator:
    """
    @brief Orchestrates the project generation process by cloning template files.
    """

    def __init__(self, loader: TemplateLoader, renderer: TemplateRenderer) -> None:
        self.loader = loader
        self.renderer = renderer

    def generate(
        self,
        project_name: str,
        template_name: str,
        output_dir: str,
        extra_placeholders: dict[str, str] | None = None,
    ) -> str:
        """
        @brief Generates a new application structure under output_dir/project_name/
        @return The absolute path of the generated project.
        """
        template_path = self.loader.get_template_path(template_name)

        output_dir_real = os.path.realpath(output_dir)
        project_path = os.path.join(output_dir, project_name)
        project_path_real = os.path.realpath(project_path)

        if os.path.commonpath([output_dir_real, project_path_real]) != output_dir_real:
            raise PathTraversalError(f"Path traversal detected in project_name: {project_name}")

        os.makedirs(project_path_real, exist_ok=True)

        placeholders = {
            "project_name": project_name,
            "package_name": project_name.lower().replace("-", "_"),
            "author": "Developer",
            "python_version": "3.13",
        }
        if extra_placeholders:
            placeholders.update(extra_placeholders)

        for root, dirs, files in os.walk(template_path):
            relative_dir = os.path.relpath(root, template_path)
            if relative_dir == ".":
                dest_dir = project_path_real
            else:
                rendered_rel_dir = self.renderer.render(relative_dir, placeholders)
                dest_dir = os.path.join(project_path_real, rendered_rel_dir)

            dest_dir_real = os.path.realpath(dest_dir)
            if os.path.commonpath([project_path_real, dest_dir_real]) != project_path_real:
                raise PathTraversalError(f"Path traversal detected in directory generation: {rendered_rel_dir}")

            os.makedirs(dest_dir_real, exist_ok=True)

            for file in files:
                src_file_path = os.path.join(root, file)
                rendered_file_name = self.renderer.render(file, placeholders)
                dest_file_path = os.path.join(dest_dir_real, rendered_file_name)

                dest_file_path_real = os.path.realpath(dest_file_path)
                if os.path.commonpath([project_path_real, dest_file_path_real]) != project_path_real:
                    raise PathTraversalError(f"Path traversal detected in file generation: {rendered_file_name}")

                try:
                    with open(src_file_path, "r", encoding="utf-8") as f:
                        file_content = f.read()
                    rendered_content = self.renderer.render(file_content, placeholders)
                    with open(dest_file_path_real, "w", encoding="utf-8") as f:
                        f.write(rendered_content)
                except UnicodeDecodeError:
                    # Binary file, copy raw
                    shutil.copy2(src_file_path, dest_file_path_real)

        return project_path_real
