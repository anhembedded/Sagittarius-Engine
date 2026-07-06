from unittest.mock import MagicMock, patch

from src.modules.database_module import DatabaseModule


def test_database_module_no_sqlalchemy():
    with patch("src.modules.database_module.SQLALCHEMY_INSTALLED", False):
        module = DatabaseModule()
        mock_app = MagicMock()
        mock_logger = MagicMock()
        mock_app.container.resolve.return_value = mock_logger

        module.register(mock_app)
        mock_logger.warning.assert_called()
