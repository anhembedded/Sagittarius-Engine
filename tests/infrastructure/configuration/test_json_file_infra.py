import pytest
import os
import json
from src.infrastructure.configuration.Json_File_Infra import JsonFileInfra

def test_json_file_infra_singleton():
    infra1 = JsonFileInfra()
    infra2 = JsonFileInfra()
    assert infra1 is infra2

def test_json_file_infra_read_write(tmp_path):
    infra = JsonFileInfra()
    file_path = tmp_path / "test.json"

    data = {"a": 1, "b": "two"}
    infra.write_json(str(file_path), data)

    read_data = infra.read_json(str(file_path))
    assert read_data == data

def test_json_file_infra_read_not_found():
    infra = JsonFileInfra()
    with pytest.raises(FileNotFoundError):
        infra.read_json("nonexistent_file.json")

def test_json_file_infra_load_json(tmp_path):
    infra = JsonFileInfra()
    file_path = tmp_path / "test.json"

    data = {"a": 1, "b": "two"}
    infra.write_json(str(file_path), data)

    loaded_data = infra.load_json(str(file_path))
    assert loaded_data == [{"key": "a", "value": 1}, {"key": "b", "value": "two"}]

def test_json_file_infra_load_json_invalid_type(tmp_path):
    infra = JsonFileInfra()
    file_path = tmp_path / "test.json"

    # Write a list instead of a dict
    with open(file_path, "w") as f:
        json.dump([1, 2, 3], f)

    with pytest.raises(TypeError):
        infra.load_json(str(file_path))
