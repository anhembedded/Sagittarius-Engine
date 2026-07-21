from typing import Any, TypeVar
from sagittarius_engine.extensions.persistence.i_session import ISession

T = TypeVar("T")


class MockSession(ISession):
    def commit(self) -> None:
        print("💾 [MockSession] Transaction committed successfully!")

    def rollback(self) -> None:
        print("🧹 [MockSession] Transaction rolled back due to error!")

    def execute(self, statement: Any, params: Any = None) -> Any:
        pass

    def query(self, *entities: Any) -> Any:
        pass

    def add(self, entity: Any) -> None:
        pass

    def get(self, entity_class: type[T], entity_id: Any) -> T | None:
        return None

    def merge(self, entity: Any) -> Any:
        return entity

    def delete(self, entity: Any) -> None:
        pass
