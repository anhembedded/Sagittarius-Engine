from unittest.mock import MagicMock, patch
from sagittarius_engine.extensions.health_module import HealthModule

def test_health_module_register():
    # Patch abstract methods so we can instantiate HealthModule without implementing boot
    with patch.object(HealthModule, "__abstractmethods__", set()):
        module = HealthModule()
        mock_context = MagicMock()

        # Test that register can be called without errors
        module.register(mock_context)
