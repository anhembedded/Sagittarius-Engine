import os
import pytest
from unittest.mock import patch
from sagittarius_engine.infrastructure.storage.local_file_storage import LocalFileStorage
from sagittarius_engine.exceptions import PathTraversalError

def test_local_file_storage_vuln__commonpath_prefix_bypass__raises_error(tmp_path):
    """
    Test that even if os.path.commonpath returns the base path (due to prefix matching like /tmp/folder vs /tmp/folder2),
    the LocalFileStorage still strictly blocks it via startswith check.
    """
    # We will simulate a scenario where commonpath incorrectly allows it (or rather, we test the vulnerability behavior directly).
    # Since commonpath behaviour is OS specific and standard, we will just use the exact path combinations known to cause it if we don't use strict joining,
    # or we can patch commonpath. Actually, the easiest way is to mock realpath and commonpath to simulate the specific prefix bypass condition.

    storage = LocalFileStorage("/tmp/folder")

    with patch("os.path.realpath") as mock_realpath, \
         patch("os.path.commonpath") as mock_commonpath:

        # Simulate base_path resolving to /tmp/folder
        # Simulate full_path resolving to /tmp/folder2/file.txt
        def side_effect_realpath(path):
            if path == "/tmp/folder":
                return "/tmp/folder"
            return "/tmp/folder2/file.txt"

        mock_realpath.side_effect = side_effect_realpath

        # Simulate commonpath mistakenly thinking /tmp/folder2/file.txt is within /tmp/folder.
        # Actually standard commonpath would return /tmp, which fails the first check.
        # The vulnerability specifically happens if developers used os.path.commonprefix, OR if they used commonpath but expected it to validate strictly.
        # Wait, os.path.commonpath(['/tmp/folder', '/tmp/folder2']) returns '/tmp', which is NOT '/tmp/folder'.
        # So os.path.commonpath actually prevents this specific prefix bypass natively!
        # The prompt says: "The use of os.path.commonpath for checking if a path is within another is known to be vulnerable unless an os.sep is appended, as it just matches path prefixes."
        # While commonpath *does* resolve components, we still need to test our added logic works for the exact case.

        # Let's mock commonpath to return base_path to trigger our secondary check.
        mock_commonpath.return_value = "/tmp/folder"

        with pytest.raises(PathTraversalError):
            storage._get_full_path("../folder2/file.txt")

def test_local_file_storage_vuln__valid_paths__allowed():
    storage = LocalFileStorage("/tmp/folder")
    with patch("os.path.realpath") as mock_realpath, \
         patch("os.path.commonpath") as mock_commonpath, \
         patch("os.path.exists") as mock_exists:

        def side_effect_realpath(path):
            if path == "/tmp/folder":
                return "/tmp/folder"
            if path == "/tmp/folder/file.txt":
                return "/tmp/folder/file.txt"
            return path

        mock_realpath.side_effect = side_effect_realpath
        mock_commonpath.return_value = "/tmp/folder"

        # Should not raise exception
        result = storage._get_full_path("file.txt")
        assert result == "/tmp/folder/file.txt"
