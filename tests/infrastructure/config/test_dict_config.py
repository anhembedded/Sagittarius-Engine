import pytest
from sagittarius_engine.infrastructure.config.dict_config import DictConfig


def test_dict_config_initialization_empty():
    config = DictConfig()
    assert config._config == {}


def test_dict_config_initialization_with_data():
    initial_data = {"key1": "value1", "key2": 123}
    config = DictConfig(initial_data=initial_data)
    assert config._config == initial_data
