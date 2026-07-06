from unittest.mock import MagicMock

import pytest

from src.base_repository import BaseRepository


class MyEntity:
    def __init__(self, id):
        self.id = id


def test_base_repository():
    mock_session = MagicMock()
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)

    # Test internal methods
    assert repo.session == mock_session
    assert repo.entity_class == MyEntity

    # Test some basic stuff
    entity = MyEntity(1)

    # get_by_id branch 1
    mock_session.session.get.return_value = entity
    assert repo.get_by_id(1) == entity

    # get_by_id branch 1 - not found
    mock_session.session.get.return_value = None
    assert repo.get_by_id(999) is None

    # get_by_id branch 2
    del mock_session.session
    mock_session.query.return_value.get.return_value = entity
    assert repo.get_by_id(1) == entity

    # get_by_id branch 2 - not found
    mock_session.query.return_value.get.return_value = None
    assert repo.get_by_id(999) is None

    # add branch 1
    mock_session = MagicMock()
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)
    repo.add(entity)
    mock_session.session.add.assert_called_with(entity)

    # list_all
    mock_session.query.return_value.all.return_value = [entity]
    assert repo.list_all() == [entity]

    # update branch 1
    repo.update(entity)
    mock_session.session.merge.assert_called_with(entity)

    # delete branch 1
    repo.delete(entity)
    mock_session.session.delete.assert_called_with(entity)


def test_base_repository_exceptions():
    mock_session = MagicMock()
    del mock_session.session
    del mock_session.query
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)

    entity = MyEntity(1)

    with pytest.raises(NotImplementedError):
        repo.add(entity)

    with pytest.raises(NotImplementedError):
        repo.get_by_id(1)

    with pytest.raises(NotImplementedError):
        repo.list_all()

    # update branch 2 (does nothing)
    repo.update(entity)

    with pytest.raises(NotImplementedError):
        repo.delete(entity)
