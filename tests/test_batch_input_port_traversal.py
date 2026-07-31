import os
import pytest
from sagittarius_engine.adapters.batch.batch_input_port import BatchInputPort
from sagittarius_engine.exceptions import PathTraversalError

def test_batch_input_port_traversal_blocked(tmp_path):
    base_dir = tmp_path / "base"
    base_dir.mkdir()

    # Try to traverse out
    with pytest.raises(PathTraversalError):
        BatchInputPort(
            file_path="../../etc/passwd",
            base_path=str(base_dir)
        )

def test_batch_input_port_valid_path(tmp_path):
    base_dir = tmp_path / "base"
    base_dir.mkdir()

    # Valid relative path should not raise PathTraversalError
    port = BatchInputPort(
        file_path="valid.csv",
        base_path=str(base_dir)
    )
    assert os.path.basename(port.file_path) == "valid.csv"
