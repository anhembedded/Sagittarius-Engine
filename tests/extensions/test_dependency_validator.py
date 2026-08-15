import pytest
from unittest.mock import MagicMock, patch
from sagittarius_engine.extensions.dependency_validator import (
    DependencyValidatorExtension,
)


@pytest.fixture
def mock_context():
    from sagittarius_engine.interfaces.i_logger import ILogger

    context = MagicMock()
    context.logger = MagicMock(spec=ILogger)
    return context


@patch("importlib.util.find_spec")
def test_dependency_validator_success(mock_find_spec, mock_context):
    # Mock find_spec to always return True (module exists)
    mock_find_spec.return_value = True

    extension = DependencyValidatorExtension(required_packages=["existing_pkg"])

    # Should not raise SystemExit
    extension.boot(mock_context)

    # Verify logger was called with INFO
    mock_context.logger.info.assert_called_with(
        "Pre-flight check passed. All critical dependencies found."
    )
    mock_context.logger.error.assert_not_called()


@patch("importlib.util.find_spec")
@patch("sys.exit")
def test_dependency_validator_failure(mock_exit, mock_find_spec, mock_context):
    # Mock find_spec to return None (module missing) for a specific package
    def mock_find_spec_side_effect(pkg):
        if pkg == "missing_pkg":
            return None
        return True

    mock_find_spec.side_effect = mock_find_spec_side_effect

    extension = DependencyValidatorExtension(
        required_packages=["existing_pkg", "missing_pkg"]
    )

    extension.boot(mock_context)

    # Verify logger was called with ERROR
    mock_context.logger.error.assert_called()
    critical_msg = mock_context.logger.error.call_args[0][0]

    assert "CRITICAL FAULT: Missing required dependencies: missing_pkg" in critical_msg
    assert "pip install missing_pkg" in critical_msg

    # Verify sys.exit was called with 1
    mock_exit.assert_called_once_with(1)
