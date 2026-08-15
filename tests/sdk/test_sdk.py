import os
import subprocess
import sys

import pytest

from sagittarius_engine.sdk.project_generator import ProjectGenerator
from sagittarius_engine.sdk.template_loader import TemplateLoader
from sagittarius_engine.sdk.template_renderer import TemplateRenderer


def test_template_loader_discovery(tmp_path):
    loader = TemplateLoader()
    templates = loader.list_templates()
    assert "minimal" in templates
    assert "clean" in templates
    assert "ddd" in templates
    assert "mvc" in templates

    # Test dynamic registration
    custom_dir = tmp_path / "custom_templates"
    custom_dir.mkdir()
    tpl_dir = custom_dir / "my_custom_tpl"
    tpl_dir.mkdir()
    (tpl_dir / "main.py").write_text("print('hello')")

    loader.register_template_directory(str(custom_dir))
    assert "my_custom_tpl" in loader.list_templates()
    assert loader.get_template_path("my_custom_tpl") == str(tpl_dir)

    with pytest.raises(ValueError):
        loader.get_template_path("non_existent_template_999")


def test_template_renderer():
    renderer = TemplateRenderer()
    content = "Project: {{ project_name }}, Author: {{author}}, Version: {{ version }}"
    placeholders = {
        "project_name": "MyProj",
        "author": "Alice",
        "version": "1.2.3",
    }
    rendered = renderer.render(content, placeholders)
    assert rendered == "Project: MyProj, Author: Alice, Version: 1.2.3"

    # Test with spacing variations
    content_space = "{{project_name}} - {{  author  }}"
    assert renderer.render(content_space, placeholders) == "MyProj - Alice"


def test_project_generator(tmp_path):
    loader = TemplateLoader()
    renderer = TemplateRenderer()
    generator = ProjectGenerator(loader, renderer)

    project_name = "test-generated-app"
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Generate minimal project
    project_path = generator.generate(
        project_name=project_name,
        template_name="minimal",
        output_dir=str(output_dir),
        extra_placeholders={"author": "TestBot"},
    )

    assert os.path.exists(project_path)
    assert os.path.exists(os.path.join(project_path, "main.py"))
    assert os.path.exists(os.path.join(project_path, "config.json"))

    # Verify placeholder rendering in config.json
    with open(os.path.join(project_path, "config.json"), "r") as f:
        config_content = f.read()
    assert "test-generated-app" in config_content
    assert "TestBot" in config_content

    # Run the generated main.py using python subprocess to verify it is runnable immediately
    # We must prepend the current workspace to PYTHONPATH so the generated project can import sagittarius_engine
    env = os.environ.copy()
    current_workspace = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
    env["PYTHONPATH"] = f"{current_workspace}{os.pathsep}{env.get('PYTHONPATH', '')}"

    result = subprocess.run(
        [sys.executable, "main.py"],
        cwd=project_path,
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode == 0
    assert "booted successfully" in result.stdout
    assert "test-generated-app" in result.stdout
