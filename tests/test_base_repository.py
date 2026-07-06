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


def test_base_repository__get_by_id__success():
    mock_session = MagicMock()
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)
    entity = MyEntity(1)
    mock_session.get.return_value = entity
    assert repo.get_by_id(1) == entity
    mock_session.get.assert_called_with(MyEntity, 1)


def test_base_repository__list_all__success():
    mock_session = MagicMock()
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)
    entity = MyEntity(1)
    mock_session.query.return_value.all.return_value = [entity]
    assert repo.list_all() == [entity]

    # update branch 1
    repo.update(entity)
    mock_session.session.merge.assert_called_with(entity)

    # Note: delete branch 1 is now covered in test_base_repository__delete_supported_session__calls_session_delete
    mock_session.query.assert_called_with(MyEntity)
    mock_session.query.return_value.all.assert_called_once()


def test_base_repository__update__success():
    mock_session = MagicMock()
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)
    entity = MyEntity(1)
    repo.update(entity)
    mock_session.merge.assert_called_with(entity)

    # Note: delete exception is now covered in test_base_repository__delete_unsupported_session__raises_not_implemented_error


def test_base_repository__delete_supported_session__calls_session_delete():
    mock_session = MagicMock()
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)
    entity = MyEntity(1)

    repo.delete(entity)

    mock_session.session.delete.assert_called_once_with(entity)


def test_base_repository__delete_unsupported_session__raises_not_implemented_error():
    mock_session = MagicMock()
    del mock_session.session
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)
    entity = MyEntity(1)

    with pytest.raises(NotImplementedError):
        repo.delete(entity)

def test_base_repository__delete__success():
    mock_session = MagicMock()
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)
    entity = MyEntity(1)
    repo.delete(entity)
    mock_session.delete.assert_called_with(entity)
