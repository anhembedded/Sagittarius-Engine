import os
import json
import pytest
from src.infrastructure.configuration.Json_File_Infra import JsonFileInfra

@pytest.fixture(autouse=True)
def reset_singleton():
    JsonFileInfra._instance = None

def test_json_file_infra_singleton():
    infra1 = JsonFileInfra()
    infra2 = JsonFileInfra()
    assert infra1 is infra2

def test_json_file_infra_write_and_read(tmp_path):
    infra = JsonFileInfra()
    file_path = tmp_path / "test.json"
    data = {"key": "value"}

    infra.write_json(str(file_path), data)

    assert file_path.exists()

    read_data = infra.read_json(str(file_path))
    assert read_data == data

def test_json_file_infra_read_not_found(tmp_path):
    infra = JsonFileInfra()
    file_path = tmp_path / "nonexistent.json"

    with pytest.raises(FileNotFoundError):
        infra.read_json(str(file_path))

def test_json_file_infra_load_json_valid(tmp_path):
    infra = JsonFileInfra()
    file_path = tmp_path / "test2.json"
    data = {"a": 1, "b": 2}
    infra.write_json(str(file_path), data)

    result = infra.load_json(str(file_path))
    assert result == [{"key": "a", "value": 1}, {"key": "b", "value": 2}]

def test_json_file_infra_load_json_invalid_type(tmp_path):
    infra = JsonFileInfra()
    file_path = tmp_path / "test3.json"
    with open(file_path, 'w') as f:
        json.dump([1, 2, 3], f)

    with pytest.raises(TypeError):
        infra.load_json(str(file_path))
