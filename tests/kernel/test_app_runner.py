import pytest
from unittest.mock import MagicMock, patch

try:
    from sagittarius_engine.kernel.app_runner import AppRunner
except ImportError:
    AppRunner = None  # type: ignore

pytestmark = pytest.mark.skipif(
    AppRunner is None,
    reason="AppRunner snippet not present in local evaluation environment",
)

def test_app_runner_init():
    mock_app = MagicMock()
    runner = AppRunner(app=mock_app)
    assert runner.app == mock_app

def test_app_runner_run_cli_loop():
    mock_app = MagicMock()
    runner = AppRunner(app=mock_app)

    with patch("builtins.input", side_effect=["test_cmd", "exit"]) as mock_input:
        runner.run_cli_loop()

    mock_app.dispatch.assert_called_once_with("test_cmd")
    assert mock_input.call_count == 2
