from unittest.mock import MagicMock


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

    # Test CRUD operations
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

    # test delete
    repo.delete(entity)
    mock_session.delete.assert_called_with(entity)
