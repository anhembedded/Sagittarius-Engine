import os
import pytest

from sagittarius_engine.infrastructure.storage.local_file_storage import LocalFileStorage
from sagittarius_engine.exceptions import PathTraversalError


@pytest.fixture
def base_dir(tmp_path):
    """Fixture providing a temporary base directory for the file storage."""
    base = tmp_path / "storage_base"
    base.mkdir()
    return str(base)


@pytest.fixture
def storage(base_dir):
    """Fixture providing a LocalFileStorage instance."""
    return LocalFileStorage(base_path=base_dir)


def test_local_file_storage__read_write_valid_path__success(storage, base_dir):
    """Test reading and writing within the allowed base directory."""
    test_path = "subfolder/test_file.txt"
    data = "Hello, Storage!"

    # Write data
    storage.write(test_path, data)

    # Check if exists
    assert storage.exists(test_path) is True

    # Read data
    read_data = storage.read(test_path)
    assert read_data == data.encode('utf-8')

    # Delete data
    storage.delete(test_path)
    assert storage.exists(test_path) is False


def test_local_file_storage__path_traversal__raises_error(storage):
    """Test that attempting to use ../ to escape the base path raises PathTraversalError."""
    malicious_path = "../escaped_file.txt"

    with pytest.raises(PathTraversalError):
        storage._get_full_path(malicious_path)

    with pytest.raises(PathTraversalError):
        storage.read(malicious_path)

    with pytest.raises(PathTraversalError):
        storage.write(malicious_path, b"malicious data")


def test_local_file_storage__absolute_path__raises_error(storage):
    """Test that attempting to read an absolute path outside base path raises PathTraversalError."""
    malicious_path = "/etc/passwd"

    with pytest.raises(PathTraversalError):
        storage._get_full_path(malicious_path)


def test_local_file_storage__symlink_escape__raises_error(storage, base_dir, tmp_path):
    """Test that using a symlink to escape the base directory raises PathTraversalError."""
    # Create a target file outside the base directory
    target_file = tmp_path / "secret.txt"
    target_file.write_text("Secret Data")

    # Create a symlink inside the base directory pointing to the external file
    symlink_path = os.path.join(base_dir, "symlink.txt")
    try:
        os.symlink(str(target_file), symlink_path)
    except OSError as e:
        if getattr(e, "winerror", None) == 1314:
            pytest.skip("Developer privilege for creating symlinks is not held on Windows.")
        raise

    # Attempt to read through the symlink (the path 'symlink.txt' is relative to base_dir)
    with pytest.raises(PathTraversalError):
        storage.read("symlink.txt")


def test_local_file_storage__none_path__raises_value_error(storage):
    """Test that providing None as a path raises ValueError."""
    with pytest.raises(ValueError, match="Path cannot be None"):
        storage._get_full_path(None)


def test_local_file_storage__empty_path__resolves_to_base_dir(storage, base_dir):
    """Test that an empty path resolves to the base directory itself."""
    resolved_path = storage._get_full_path("")
    assert resolved_path == os.path.realpath(base_dir)
