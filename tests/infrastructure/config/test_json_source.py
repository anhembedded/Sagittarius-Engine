import json

from sagittarius_engine.infrastructure.config.json_source import JsonSource


def test_json_source_init():
    """Test that JsonSource correctly initializes with a filepath."""
    filepath = "/fake/path/config.json"
    source = JsonSource(filepath)
    assert source.filepath == filepath


def test_json_source_read_valid_json(tmp_path):
    """Test reading a valid JSON file."""
    config_data = {"key1": "value1", "key2": 42}
    config_file = tmp_path / "valid_config.json"
    config_file.write_text(json.dumps(config_data))

    source = JsonSource(str(config_file))
    result = source.read()

    assert result == config_data


def test_json_source_read_non_existent_file(tmp_path):
    """Test reading a file that does not exist."""
    missing_file = tmp_path / "missing_config.json"
    source = JsonSource(str(missing_file))

    result = source.read()

    assert result == {}


def test_json_source_read_invalid_json(tmp_path):
    """Test reading a file with invalid JSON."""
    invalid_file = tmp_path / "invalid_config.json"
    invalid_file.write_text("{invalid json format]")

    source = JsonSource(str(invalid_file))
    result = source.read()

    assert result == {}
