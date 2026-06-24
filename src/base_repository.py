from typing import Generic, TypeVar, Any, List, Optional
from src.interfaces import ISession

T = TypeVar('T')

class BaseRepository(Generic[T]):
    """
    @brief Base generic Repository for entity CRUD operations.

    @details Provides standard add, get_by_id, list_all, update, and delete methods.
    Requires an ISession instance to perform database operations.

    @par Tutorial / Usage Example:
    @code
    class UserRepository(BaseRepository[User]):
        def __init__(self, session: ISession):
            super().__init__(session, User)

    # Usage:
    # user_repo = UserRepository(session)
    # user_repo.add(User(name="Alice"))
    # user = user_repo.get_by_id(1)
    @endcode
    """

    def __init__(self, session: ISession, entity_class: type[T]) -> None:
        """
        @brief Constructor.

        @param session The database session.
        @param entity_class The class of the entity this repository manages.
        """
        self.session = session
        self.entity_class = entity_class

    def add(self, entity: T) -> None:
        """
        @brief Adds a new entity to the database.
        @param entity The entity to add.
        """
        # Note: Depending on the underlying session type (e.g. SQLAlchemy),
        # we might need to access the underlying session object if ISession doesn't expose add.
        # Here we assume the adapter or session has an `add` method, or we use `execute`.
        if hasattr(self.session, 'session') and hasattr(self.session.session, 'add'):
            self.session.session.add(entity)
        else:
            raise NotImplementedError("Session does not support 'add' operation.")

    def get_by_id(self, entity_id: Any) -> Optional[T]:
        """
        @brief Retrieves an entity by its ID.

        @param entity_id The ID of the entity.
        @return The entity if found, otherwise None.
        """
        if hasattr(self.session, 'session') and hasattr(self.session.session, 'get'):
            return self.session.session.get(self.entity_class, entity_id)
        elif hasattr(self.session, 'query'):
            # Fallback for older SQLAlchemy versions
            return self.session.query(self.entity_class).get(entity_id)
        else:
            raise NotImplementedError("Session does not support 'get' operation.")

    def list_all(self) -> List[T]:
        """
        @brief Lists all entities of this type.
        @return A list of entities.
        """
        if hasattr(self.session, 'query'):
            return self.session.query(self.entity_class).all()
        else:
            raise NotImplementedError("Session does not support 'query' operation.")

    def update(self, entity: T) -> None:
        """
        @brief Updates an existing entity.
        @param entity The entity to update.
        """
        # In many ORMs like SQLAlchemy, objects attached to the session are automatically updated on commit.
        # If explicit merge/update is needed:
        if hasattr(self.session, 'session') and hasattr(self.session.session, 'merge'):
            self.session.session.merge(entity)
        else:
            pass # Trust session tracking

    def delete(self, entity: T) -> None:
        """
        @brief Deletes an entity.
        @param entity The entity to delete.
        """
        if hasattr(self.session, 'session') and hasattr(self.session.session, 'delete'):
            self.session.session.delete(entity)
        else:
            raise NotImplementedError("Session does not support 'delete' operation.")
