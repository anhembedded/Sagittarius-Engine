---
type: design_doc
tags: [sagittarius, repository]
language: python
---

# BaseRepository

## Overview
`BaseRepository` provides a generic implementation of the Repository pattern for standard Create, Read, Update, and Delete (CRUD) operations. It abstracts away the direct usage of a database session for entity management.

## Problem Statement
In Clean Architecture, domain services interact with repositories via interfaces. Writing repetitive CRUD boilerplate for every entity (User, Product, Order) violates the DRY (Don't Repeat Yourself) principle.

## Proposed Solution
Sagittarius provides a generic `BaseRepository[T]` that requires an `ISession` and the target entity class upon instantiation. It utilizes reflection/duck-typing to interact with the underlying database session (primarily designed with SQLAlchemy in mind, though abstract enough to be adapted). Developers can inherit from this class to rapidly scaffold entity-specific repositories.

## Core API / Interface

### `class BaseRepository(Generic[T])` (in `src/base_repository.py`)
- `def __init__(self, session: ISession, entity_class: type[T]) -> None`: Injects the active database session and stores the managed entity type.
- `def add(self, entity: T) -> None`: Adds a new entity to the database.
- `def get_by_id(self, entity_id: Any) -> Optional[T]`: Retrieves an entity by its primary key ID.
- `def list_all(self) -> List[T]`: Retrieves a list of all entities of this type.
- `def update(self, entity: T) -> None`: Updates an existing entity.
- `def delete(self, entity: T) -> None`: Deletes an entity.

## Dependencies
- Internal: `ISession`
- External: Standard libraries (`typing.Generic`, `typing.TypeVar`)

## How to Use / Examples

```python
from src.base_repository import BaseRepository
from src.interfaces import ISession

# Assume User is an ORM entity class
class User:
    pass

class UserRepository(BaseRepository[User]):
    """
    UserRepository automatically inherits add, get_by_id, list_all, update, delete
    """
    def __init__(self, session: ISession):
        super().__init__(session, User)

    def get_by_email(self, email: str) -> User:
        # Custom domain-specific repository method
        return self.session.query(self.entity_class).filter_by(email=email).first()

# Usage
# session_mock = get_db_session()
# user_repo = UserRepository(session_mock)
# user_repo.add(User(name="Alice"))
# user = user_repo.get_by_id(1)
```

## Implementation Notes
- **Duck-Typing the Session**: The implementation checks for `session.session.add` or `session.query` to accommodate different underlying ORM structures (like raw SQLAlchemy Sessions vs scoped sessions vs AsyncSessions). If the session object does not match expectations, it will raise `NotImplementedError`.
- **Updates**: By default, the `update` method attempts to call `session.merge(entity)`. If the session does not support `merge`, it relies on the ORM's built-in change tracking mechanism (where changes to attached objects are automatically flushed on commit).

## Related Documents
- `modules.md` (DatabaseModule typically provisions the `ISession`)
