from unittest.mock import MagicMock
from src.base_repository import BaseRepository


class MyEntity:
    def __init__(self, id):
        self.id = id


def test_base_repository__init__sets_attributes():
    mock_session = MagicMock()
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)
    assert repo.session == mock_session
    assert repo.entity_class == MyEntity


def test_base_repository__add__success():
    mock_session = MagicMock()
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)
    entity = MyEntity(1)
    repo.add(entity)
    mock_session.add.assert_called_with(entity)


    # get_by_id branch 1 - not found
    mock_session.session.get.return_value = None
    assert repo.get_by_id(999) is None

    # get_by_id branch 2
    del mock_session.session
    mock_session.query.return_value.get.return_value = entity
def test_base_repository__get_by_id__success():
    mock_session = MagicMock()
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)
    entity = MyEntity(1)
    mock_session.get.return_value = entity
    assert repo.get_by_id(1) == entity
    mock_session.get.assert_called_with(MyEntity, 1)


    # get_by_id branch 2 - not found
    mock_session.query.return_value.get.return_value = None
    assert repo.get_by_id(999) is None

    # add branch 1
def test_base_repository__list_all__success():
    mock_session = MagicMock()
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)
    entity = MyEntity(1)
    mock_session.query.return_value.all.return_value = [entity]
    assert repo.list_all() == [entity]
    mock_session.query.assert_called_with(MyEntity)
    mock_session.query.return_value.all.assert_called_once()


def test_base_repository__update__success():
    mock_session = MagicMock()
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)
    entity = MyEntity(1)
    repo.update(entity)
    mock_session.merge.assert_called_with(entity)


def test_base_repository__delete__success():
    mock_session = MagicMock()
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)
    entity = MyEntity(1)
    repo.delete(entity)
    mock_session.delete.assert_called_with(entity)
