import threading
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class _Registration:
    handle: Any
    dispose: Callable[[], None]


class ResourceScope:
    """
    @brief Tracks resources acquired during one "run" of a long-lived,
    re-used object (e.g. a chart repeatedly rebuilding its indicator set)
    and disposes them together, so teardown is a property of a data
    structure instead of a convention every new call-site has to remember.

    @details Pure Python, no Qt dependency — usable anywhere a long-lived
    object accumulates per-run resources, not just in UI code. `dispose`
    callables touching Qt widgets are the caller's responsibility to only
    ever invoke on the main thread (see BOT-068); ResourceScope itself has
    no thread affinity of its own.

    Usage:
        scope = ResourceScope()
        scope.add(qualified_name, dispose=functools.partial(card.remove_indicator, qualified_name))
        ...
        previous_scope.dispose_all()
    """

    def __init__(self) -> None:
        self._registrations: list[_Registration] = []
        self._lock = threading.Lock()

    def add(self, handle: Any, dispose: Callable[[], None]) -> None:
        """
        @brief Registers one resource and the named callable that releases
        it. `dispose` must be a real function/method (never a `lambda`) so
        it shows up by name in a stack trace if teardown fails.
        """
        with self._lock:
            self._registrations.append(_Registration(handle, dispose))

    def dispose_all(self) -> None:
        """
        @brief Releases every registered resource in LIFO order (last
        registered, first disposed — a resource registered after another
        that contains it, like a curve inside a subplot row, is torn down
        first).
        @details Idempotent: safe to call repeatedly, including on an
        already-empty scope — each resource is popped off before its
        `dispose` runs, so it can never be disposed twice even if
        `dispose_all()` overlaps or gets called again. One `dispose`
        raising does not stop the rest from running — every remaining
        resource still gets its turn, and any exceptions collected along
        the way are re-raised together as an `ExceptionGroup` only after
        every resource has been attempted, so a caller wrapped in
        `safe_ui_action` (BOT-066) still logs/emits the failure instead of
        losing it.
        """
        errors: list[Exception] = []
        while True:
            with self._lock:
                if not self._registrations:
                    break
                registration = self._registrations.pop()
            try:
                registration.dispose()
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        if errors:
            raise ExceptionGroup("ResourceScope teardown failed", errors)
