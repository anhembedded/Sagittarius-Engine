import os
import json
import pytest
from src.infrastructure.configuration.Json_File_Infra import JsonFileInfra

def test_json_file_infra_read_write(tmp_path):
    infra = JsonFileInfra()
    test_file = tmp_path / "test.json"
    data = {"key": "value"}

    infra.write_json(str(test_file), data)
    assert os.path.exists(test_file)

    read_data = infra.read_json(str(test_file))
    assert read_data == data

def test_json_file_infra_file_not_found():
    infra = JsonFileInfra()
    with pytest.raises(FileNotFoundError):
        infra.read_json("non_existent_file.json")

def test_json_file_infra_singleton():
    infra1 = JsonFileInfra()
    infra2 = JsonFileInfra()
    assert infra1 is infra2
