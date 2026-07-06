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
    # Test CRUD operations
    entity = MyEntity(1)
    repo.add(entity)
    mock_session.session.add.assert_called_with(entity)


def test_base_repository__add__missing_add_method__raises_error():
    mock_session = MagicMock()
    del mock_session.session
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)
    entity = MyEntity(1)
    with pytest.raises(NotImplementedError, match="Session does not support 'add' operation."):
        repo.add(entity)


def test_base_repository__get_by_id__using_session_get__returns_entity():
    mock_session = MagicMock()
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)
    entity = MyEntity(1)
    mock_session.session.get.return_value = entity
    assert repo.get_by_id(1) == entity
    mock_session.session.get.assert_called_with(MyEntity, 1)


def test_base_repository__get_by_id__using_query_get__returns_entity():
    mock_session = MagicMock()
    del mock_session.session
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)
    entity = MyEntity(1)
    mock_session.query.return_value.get.return_value = entity
    assert repo.get_by_id(1) == entity
    mock_session.query.assert_called_with(MyEntity)
    mock_session.query.return_value.get.assert_called_with(1)


def test_base_repository__get_by_id__missing_get_and_query__raises_error():
    mock_session = MagicMock()
    del mock_session.session
    del mock_session.query
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)
    with pytest.raises(NotImplementedError, match="Session does not support 'get' operation."):
        repo.get_by_id(1)


def test_base_repository__list_all__using_query__returns_entities():
    mock_session = MagicMock()
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)
    entity = MyEntity(1)
    mock_session.query.return_value.all.return_value = [entity]
    assert repo.list_all() == [entity]
    mock_session.query.assert_called_with(MyEntity)
    mock_session.query.return_value.all.assert_called_once()


def test_base_repository__list_all__missing_query__raises_error():
    mock_session = MagicMock()
    del mock_session.query
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)
    with pytest.raises(NotImplementedError, match="Session does not support 'query' operation."):
        repo.list_all()


def test_base_repository__update__using_session_merge__success():
    mock_session = MagicMock()
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)
    entity = MyEntity(1)
    # test add
    repo.add(entity)
    mock_session.add.assert_called_with(entity)

    # test get_by_id
    mock_session.get.return_value = entity
    assert repo.get_by_id(1) == entity
    mock_session.get.assert_called_with(MyEntity, 1)

    # test list_all
    mock_session.query.return_value.all.return_value = [entity]
    assert repo.list_all() == [entity]
    mock_session.query.assert_called_with(MyEntity)

    # test update
    repo.update(entity)
    mock_session.merge.assert_called_with(entity)


def test_base_repository__update__missing_merge_method__does_nothing():
    mock_session = MagicMock()
    del mock_session.session
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)
    entity = MyEntity(1)
    repo.update(entity)
    # Ensure no exception is raised


def test_base_repository__delete__success():
    mock_session = MagicMock()
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)
    entity = MyEntity(1)
    repo.delete(entity)
    mock_session.session.delete.assert_called_with(entity)


def test_base_repository__delete__no_session_attribute__raises_error():
    mock_session = MagicMock()
    del mock_session.session
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)
    entity = MyEntity(1)
    with pytest.raises(NotImplementedError, match="Session does not support 'delete' operation."):
        repo.delete(entity)


def test_base_repository__delete__missing_delete_method__raises_error():
    mock_session = MagicMock()
    del mock_session.session.delete
    repo = BaseRepository(session=mock_session, entity_class=MyEntity)
    entity = MyEntity(1)
    with pytest.raises(NotImplementedError, match="Session does not support 'delete' operation."):
        repo.delete(entity)
    # test delete
    repo.delete(entity)
    mock_session.delete.assert_called_with(entity)
