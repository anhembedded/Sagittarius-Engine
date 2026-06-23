import pytest
import os
import json
from src.infra.config_manager import ConfigManager, DictSource, EnvSource, JsonSource

def test_config_manager_dict_source():
    manager = ConfigManager()
    manager.add_source(DictSource({"key1": "value1", "key2": 2}))

    assert manager.get("key1") == "value1"
    assert manager.get("key2") == 2
    assert manager.get("key3", "default") == "default"

def test_config_manager_env_source(monkeypatch):
    monkeypatch.setenv("APP_CONFIG_KEY", "env_value")
    manager = ConfigManager()
    manager.add_source(EnvSource(prefix="APP_CONFIG_"))

    assert manager.get("KEY") == "env_value"

def test_config_manager_json_source(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps({"json_key": "json_value"}))

    manager = ConfigManager()
    manager.add_source(JsonSource(str(config_file)))

    assert manager.get("json_key") == "json_value"

def test_config_manager_source_override():
    manager = ConfigManager()
    manager.add_source(DictSource({"shared_key": "from_dict"}))
    manager.add_source(DictSource({"shared_key": "from_second_dict", "other_key": "other"}))

    assert manager.get("shared_key") == "from_second_dict"
    assert manager.get("other_key") == "other"

def test_config_manager_set():
    manager = ConfigManager()
    manager.set("new_key", "new_value")

    assert manager.get("new_key") == "new_value"
