"""Tests for from_qml() (BOT-070, Sagittarius-Engine "lớp lỗi E").

Goes through a real QQmlEngine round-trip rather than hand-building a
QJSValue-shaped double — a hand-built Python dict passed directly bypasses
exactly the marshaling PySide6 does for a real QML JS object literal, which
is why the test suite BOT-047 shipped didn't catch the QJSValue bug BOT-061
had to fix (see that task's own postmortem). A value sent from a real QML
`Component.onCompleted` block through a `@Slot("QVariant")` receiver is the
genuine article.
"""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QObject, QUrl, Slot
from PySide6.QtQml import QQmlComponent, QQmlEngine

from sagittarius_engine.extensions.pyside_mvc.runtime.qml_value_normalizer import (
    from_qml,
)


class _Receiver(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.normalized = None

    @Slot("QVariant")
    def receive(self, value) -> None:
        # Converted here, synchronously, while the QQmlEngine that produced
        # `value` is still alive — a QJSValue is only valid for the
        # lifetime of its originating engine, and that engine is a local of
        # `_normalize_from_qml()` below, gone the moment it returns. Trying
        # to call from_qml() on the raw QJSValue *after* that point silently
        # gets back None instead of the real data (verified empirically:
        # this is what happens if you defer the from_qml() call to the
        # caller instead of doing it in here).
        self.normalized = from_qml(value)


def _normalize_from_qml(qapp, js_object_literal: str):
    """Loads a throwaway QML scene that calls `receiver.receive(...)` with
    `js_object_literal` from `Component.onCompleted`, and returns the
    Python-native value `from_qml()` produced from whatever the Slot
    actually received — the real, PySide6-marshaled value, not a
    stand-in."""
    engine = QQmlEngine()
    receiver = _Receiver()
    engine.rootContext().setContextProperty("receiver", receiver)

    qml_source = f"""
    import QtQuick
    QtObject {{
        Component.onCompleted: receiver.receive({js_object_literal})
    }}
    """.encode()

    component = QQmlComponent(engine)
    component.setData(qml_source, QUrl())
    instance = component.create()
    assert component.errorString() == "", component.errorString()
    assert instance is not None
    qapp.processEvents()

    return receiver.normalized


def test_a_flat_object_literal_normalizes_to_a_plain_dict(qapp):
    result = _normalize_from_qml(qapp, '{"symbol": "BTCUSDT", "period": 20}')

    assert result == {"symbol": "BTCUSDT", "period": 20}
    assert type(result) is dict


def test_a_nested_object_normalizes_every_level(qapp):
    result = _normalize_from_qml(qapp, '{"outer": {"inner": {"value": 42}}}')

    assert result == {"outer": {"inner": {"value": 42}}}
    assert type(result["outer"]) is dict
    assert type(result["outer"]["inner"]) is dict


def test_an_array_with_a_nested_object_normalizes_every_element(qapp):
    result = _normalize_from_qml(qapp, '{"items": [1, 2, {"nested": true}]}')

    assert result == {"items": [1, 2, {"nested": True}]}
    assert type(result["items"]) is list
    assert type(result["items"][2]) is dict


def test_a_value_that_is_already_native_python_passes_through_unchanged():
    already_native = {"a": 1, "b": [1, 2, {"c": 3}]}

    assert from_qml(already_native) == already_native


def test_from_qml_is_idempotent(qapp):
    once = _normalize_from_qml(qapp, '{"a": {"b": [1, {"c": 2}]}}')

    twice = from_qml(once)

    assert once == twice
