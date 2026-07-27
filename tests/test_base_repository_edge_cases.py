import pytest
import unittest.mock
from unittest.mock import MagicMock

from sagittarius_engine.extensions.persistence import BaseRepository

class MyEntity:
    def __init__(self, id):
        self.id = id

def test_base_repository__add__integrity_error_bubbles_up():
    # Dynamically mock sqlalchemy.exc.IntegrityError to avoid requiring the actual package
    mock_sqlalchemy = MagicMock()
    mock_exc = MagicMock()

    class MockIntegrityError(Exception):
        pass

    mock_exc.IntegrityError = MockIntegrityError
    mock_sqlalchemy.exc = mock_exc

    # Patch sys.modules to simulate sqlalchemy safely
    with unittest.mock.patch.dict('sys.modules', {'sqlalchemy': mock_sqlalchemy, 'sqlalchemy.exc': mock_exc}):
        mock_session = MagicMock()
        repo = BaseRepository(session=mock_session, entity_class=MyEntity)
        entity = MyEntity(1)

        # Configure the mock session.add to raise our fake IntegrityError
        mock_session.add.side_effect = mock_sqlalchemy.exc.IntegrityError("Unique constraint failed")

        with pytest.raises(mock_sqlalchemy.exc.IntegrityError, match="Unique constraint failed"):
            repo.add(entity)

        mock_session.add.assert_called_with(entity)
