import pytest
from unittest.mock import MagicMock
from sagittarius_engine.extensions.thread_manager_module import ThreadManagerModule

def test_thread_manager_module_register():
    module = ThreadManagerModule()

    # Strictly assert what is in the snippet:
    # `def register(self, context: IEngineContext) -> None: pass`
    mock_context = MagicMock()
    result = module.register(mock_context)

    assert result is None

def test_thread_manager_module_boot():
    module = ThreadManagerModule()
    mock_app = MagicMock()
    result = module.boot(mock_app)
    assert result is None
