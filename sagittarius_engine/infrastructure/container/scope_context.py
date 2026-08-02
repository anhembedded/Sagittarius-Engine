import threading
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Generator

_current_scope: ContextVar[dict[type, Any] | None] = ContextVar(
    "_current_scope", default=None
)


class ScopeContext:
    """
    @brief Context manager that creates an isolated dependency resolution scope.

    @details Within the scope, all `scoped` registrations resolve to the same instance.
    Different scopes (e.g., different HTTP requests) receive different instances.

    Usage:
        with container.create_scope():
            session1 = container.resolve(ISession)  # new scoped instance
            session2 = container.resolve(ISession)  # same instance as session1

        with container.create_scope():
            session3 = container.resolve(ISession)  # brand-new instance
    """

    def __init__(self, scoped_registry: dict[type, type]) -> None:
        self._scoped_registry = scoped_registry
        self._token: Any = None

    def __enter__(self) -> "ScopeContext":
        self._token = _current_scope.set({})
        return self

    def __exit__(self, *args: object) -> None:
        _current_scope.reset(self._token)

    def resolve(self, abstract: type) -> Any | None:
        """
        @brief Resolves a scoped instance within the current scope.
        @return Instance if abstract is scoped and a scope is active, else None.
        """
        scope = _current_scope.get()
        if scope is None:
            return None

        concrete = self._scoped_registry.get(abstract)
        if concrete is None:
            return None

        if abstract not in scope:
            scope[abstract] = concrete()

        return scope[abstract]
