import json
from unittest.mock import MagicMock

from sagittarius_engine.infrastructure.config.config_manager import ConfigManager
from sagittarius_engine.infrastructure.config.config_source import ConfigSource


def test_config_manager_convenience_loaders(tmp_path, monkeypatch):
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps({"json_k": "json_v"}))
    monkeypatch.setenv("TEST_ENV_K", "env_v")

    manager = ConfigManager()
    manager.load_dict({"dict_k": "dict_v"})
    manager.load_json(str(config_file))
    manager.load_env("TEST_ENV_")

    assert manager.get("dict_k") == "dict_v"
    assert manager.get("json_k") == "json_v"
    assert manager.get("K") == "env_v"


def test_config_manager_from_json(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps({"json_k": "json_v"}))

    manager = ConfigManager.from_json(str(config_file))
    assert manager.get("json_k") == "json_v"


def test_config_manager_load_exception():
    manager = ConfigManager()
    broken_source = MagicMock(spec=ConfigSource)
    broken_source.read.side_effect = Exception("Failed to read")
    manager.add_source(broken_source)

    manager.load_dict({"valid_k": "valid_v"})

    # Should swallow exception and continue loading subsequent sources
    assert manager.get("valid_k") == "valid_v"


def test_config_manager_get_casting():
    manager = ConfigManager()
    manager.load_dict(
        {
            "int_str": "123",
            "float_str": "1.23",
            "invalid_int": "abc",
            "already_int": 456,
        }
    )

    # Test successful cast
    assert manager.get("int_str", cast=int) == 123
    assert manager.get("float_str", cast=float) == 1.23

    # Test invalid cast (should fallback to returning original value)
    assert manager.get("invalid_int", cast=int) == "abc"

    # Test already same type
    assert manager.get("already_int", cast=int) == 456

    # Test default
    assert manager.get("non_existent", default="def", cast=int) == "def"

    # Test TypeError (e.g., passing a list to int) falls back to original value
    manager.load_dict({"list_val": [1, 2]})
    assert manager.get("list_val", cast=int) == [1, 2]
