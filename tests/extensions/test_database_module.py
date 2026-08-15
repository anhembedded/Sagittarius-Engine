from unittest.mock import MagicMock, patch

from sagittarius_engine.extensions.persistence.database_module import DatabaseExtension


def test_database_module_no_sqlalchemy():
    with patch(
        "sagittarius_engine.extensions.persistence.database_module.SQLALCHEMY_INSTALLED",
        False,
    ):
        extension = DatabaseExtension()
        mock_app = MagicMock()
        mock_logger = MagicMock()
        mock_app.container.resolve.return_value = mock_logger

        extension.register(mock_app)
        mock_logger.warning.assert_called()
