"""Integration tests for TASK-012: DI Container Scoped Lifecycle."""

import threading

from sagittarius_engine.infrastructure.container.std_container import StdLibContainer


class IService:
    pass


class ConcreteService(IService):
    def __init__(self) -> None:
        self.id = id(self)


class TestScopedLifecycle:
    def test_scoped_resolves_same_instance_within_scope(self) -> None:
        container = StdLibContainer()
        container.scoped(IService, ConcreteService)

        with container.create_scope():
            a = container.resolve(IService)
            b = container.resolve(IService)
            assert a is b, (
                "Within a scope, scoped dependency must be the same instance."
            )

    def test_different_scopes_produce_different_instances(self) -> None:
        container = StdLibContainer()
        container.scoped(IService, ConcreteService)

        with container.create_scope():
            a = container.resolve(IService)

        with container.create_scope():
            b = container.resolve(IService)

        assert a is not b, "Different scopes must produce different instances."

    def test_concurrent_scopes_are_isolated(self) -> None:
        """Validate that two concurrent scopes (e.g., two HTTP requests) do not share instances."""
        container = StdLibContainer()
        container.scoped(IService, ConcreteService)

        # Store actual object references (not id()) to prevent CPython from reusing
        # memory addresses after one scope's ConcreteService is GC'd.
        results: list[IService] = []

        def resolve_in_scope() -> None:
            with container.create_scope():
                svc = container.resolve(IService)
                results.append(svc)

        t1 = threading.Thread(target=resolve_in_scope)
        t2 = threading.Thread(target=resolve_in_scope)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        assert len(results) == 2
        assert results[0] is not results[1], (
            "Concurrent scopes must produce different instances."
        )

    def test_outside_scope_falls_back_to_transient(self) -> None:
        """Scoped dependency outside a scope should fall back to Transient resolution."""
        container = StdLibContainer()
        container.scoped(IService, ConcreteService)

        # Outside any scope, the scoped registry is inactive → falls back to _resolve
        a = container.resolve(IService)
        b = container.resolve(IService)
        # Transient: new instance each time
        assert a is not b, "Without a scope, scoped dependency resolves as Transient."
