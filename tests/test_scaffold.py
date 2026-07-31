import json
import os
from unittest.mock import patch

from tools.scaffold import create_project


def test_scaffold_create_project_error(capsys, tmp_path):
    project_name = "test_project_error"
    base_path = str(tmp_path)

    with patch("os.makedirs", side_effect=Exception("Test error")), \
         patch("builtins.open"):
        create_project(project_name, base_path)

    captured = capsys.readouterr()
    assert "Error creating project: Test error" in captured.out


def test_scaffold_create_project(tmp_path):
    project_name = "test_project"
    base_path = str(tmp_path)

    create_project(project_name, base_path)

    project_dir = os.path.join(base_path, project_name)
    assert os.path.exists(project_dir)
    assert os.path.exists(os.path.join(project_dir, "modules", "__init__.py"))

    config_path = os.path.join(project_dir, "config.json")
    assert os.path.exists(config_path)
    with open(config_path) as f:
        config_data = json.load(f)
        assert config_data["app_name"] == project_name
        assert config_data["version"] == "1.0.0"

    main_path = os.path.join(project_dir, "main.py")
    assert os.path.exists(main_path)
    with open(main_path) as f:
        content = f.read()
        assert 'app.boot(auto_discover="modules")' in content
