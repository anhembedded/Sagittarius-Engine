"""Tests for ResourceScope (BOT-067, Sagittarius-Engine "lớp lỗi C")."""

import pytest

from sagittarius_engine.runtime.tasks.resource_scope import ResourceScope


class _Recorder:
    def __init__(self) -> None:
        self.disposed: list[str] = []

    def dispose(self, name: str) -> None:
        self.disposed.append(name)


def test_dispose_all_releases_every_registered_resource():
    recorder = _Recorder()
    scope = ResourceScope()
    scope.add("a", dispose=lambda: recorder.dispose("a"))
    scope.add("b", dispose=lambda: recorder.dispose("b"))

    scope.dispose_all()

    assert set(recorder.disposed) == {"a", "b"}


def test_dispose_all_runs_in_lifo_order():
    """A resource registered after another that contains it (e.g. a curve
    inside a subplot row) must be disposed first."""
    recorder = _Recorder()
    scope = ResourceScope()
    scope.add("row", dispose=lambda: recorder.dispose("row"))
    scope.add("curve", dispose=lambda: recorder.dispose("curve"))

    scope.dispose_all()

    assert recorder.disposed == ["curve", "row"]


def test_dispose_all_is_idempotent():
    recorder = _Recorder()
    scope = ResourceScope()
    scope.add("a", dispose=lambda: recorder.dispose("a"))

    scope.dispose_all()
    scope.dispose_all()  # must not re-dispose or raise

    assert recorder.disposed == ["a"]


def test_dispose_all_on_an_empty_scope_does_nothing():
    scope = ResourceScope()

    scope.dispose_all()  # must not raise


def test_a_failing_dispose_does_not_block_the_remaining_ones():
    recorder = _Recorder()
    scope = ResourceScope()
    scope.add("a", dispose=lambda: recorder.dispose("a"))

    def _boom() -> None:
        raise ValueError("teardown exploded")

    scope.add("broken", dispose=_boom)
    scope.add("c", dispose=lambda: recorder.dispose("c"))

    with pytest.raises(ExceptionGroup) as exc_info:
        scope.dispose_all()

    # "broken" was registered between "a" and "c" — both of its LIFO
    # neighbors must still have run despite it raising.
    assert set(recorder.disposed) == {"a", "c"}
    assert len(exc_info.value.exceptions) == 1
    assert isinstance(exc_info.value.exceptions[0], ValueError)


def test_multiple_failing_disposes_are_all_collected_into_one_group():
    scope = ResourceScope()

    def _boom_one() -> None:
        raise ValueError("first")

    def _boom_two() -> None:
        raise TypeError("second")

    scope.add("a", dispose=_boom_one)
    scope.add("b", dispose=_boom_two)

    with pytest.raises(ExceptionGroup) as exc_info:
        scope.dispose_all()

    assert len(exc_info.value.exceptions) == 2


def test_after_disposal_the_scope_is_empty_so_a_retry_only_reports_new_failures():
    scope = ResourceScope()

    def _boom() -> None:
        raise ValueError("boom")

    scope.add("a", dispose=_boom)

    with pytest.raises(ExceptionGroup):
        scope.dispose_all()

    scope.dispose_all()  # already popped — no re-raise on retry
