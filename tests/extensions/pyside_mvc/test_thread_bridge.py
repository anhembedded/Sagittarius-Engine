"""Tests for safe_ui_action (BOT-066, Sagittarius-Engine "lớp lỗi B").

BOT-061 (Sagittarius_Elite_Warrior) showed the real cost of this decorator's
old behavior: a TypeError from `dict(QJSValue)` was caught, printed to
stdout, and vanished — the app didn't crash, but every value the user typed
was silently discarded. `safe_ui_action` must keep production apps from
crashing the Qt event loop, but the failure has to become observable (a
real logger call with a traceback, a structured event) and, in dev mode,
loud (re-raised) instead of swallowed unconditionally.
"""

from unittest.mock import Mock

import pytest

from sagittarius_engine.extensions.pyside_mvc.mvc.base_view import DEV_MODE_CONFIG_KEY
from sagittarius_engine.extensions.pyside_mvc.safety.thread_bridge import (
    safe_ui_action,
)
from sagittarius_engine.extensions.pyside_mvc.safety.ui_action_events import (
    UiActionFailedEvent,
)


class _FakeOwner:
    """Stands in for a BasePresenter — has the attributes safe_ui_action
    duck-types onto `args[0]` (logger/event_bus/config), nothing more."""

    def __init__(self, dev_mode: bool) -> None:
        self.logger = Mock()
        self.event_bus = Mock()
        self.config = Mock()
        self.config.get.side_effect = lambda key, default=None: (
            dev_mode if key == DEV_MODE_CONFIG_KEY else default
        )

    @safe_ui_action
    def explode(self) -> None:
        raise TypeError("dict(QJSValue) is not callable like that")


def test_dev_mode_reraises_the_exception_instead_of_swallowing_it():
    """The behavior this task exists to invert: today, nothing re-raises
    regardless of dev mode — this must fail before the fix and pass after."""
    owner = _FakeOwner(dev_mode=True)

    with pytest.raises(TypeError, match="dict.QJSValue."):
        owner.explode()


def test_production_mode_still_swallows_and_returns_none():
    """Shipped behavior must not change: dev mode off (the default) never
    lets an exception reach the Qt event loop."""
    owner = _FakeOwner(dev_mode=False)

    result = owner.explode()

    assert result is None


def test_logs_the_error_with_a_traceback_via_the_owners_logger():
    owner = _FakeOwner(dev_mode=False)

    owner.explode()

    owner.logger.error.assert_called_once()
    message, kwargs = owner.logger.error.call_args
    assert "explode" in message[0]
    traceback_text = kwargs["extra"]["traceback"]
    assert "TypeError" in traceback_text
    assert "raise TypeError" in traceback_text


def test_emits_a_structured_ui_action_failed_event():
    owner = _FakeOwner(dev_mode=False)

    owner.explode()

    owner.event_bus.emit.assert_called_once()
    (event,), _ = owner.event_bus.emit.call_args
    assert isinstance(event, UiActionFailedEvent)
    assert event.function_name == "explode"
    assert event.exception_type == "TypeError"
    assert "dict(QJSValue)" in event.message
    assert "TypeError" in event.traceback


def test_emits_the_event_in_dev_mode_too_before_reraising():
    owner = _FakeOwner(dev_mode=True)

    with pytest.raises(TypeError):
        owner.explode()

    owner.event_bus.emit.assert_called_once()


def test_still_emits_the_duck_typed_ui_log_signal_when_present():
    class _OwnerWithLogSignal(_FakeOwner):
        def __init__(self, dev_mode: bool) -> None:
            super().__init__(dev_mode)
            self.ui_log_signal = Mock()

        @safe_ui_action
        def explode(self) -> None:
            raise TypeError("boom")

    owner = _OwnerWithLogSignal(dev_mode=False)

    owner.explode()

    owner.ui_log_signal.emit.assert_called_once()
    assert "explode" in owner.ui_log_signal.emit.call_args[0][0]


def test_falls_back_to_print_without_crashing_when_there_is_no_owner(capsys):
    """safe_ui_action must keep working on a bare function with no `self`
    (args is empty) — the decorator predates BasePresenter and other
    framework consumers may still use it that way."""

    @safe_ui_action
    def bare_function() -> None:
        raise ValueError("no owner here")

    result = bare_function()

    assert result is None
    captured = capsys.readouterr()
    assert "bare_function" in captured.out
    assert "ValueError" in captured.out
