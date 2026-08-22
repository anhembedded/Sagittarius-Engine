from typing import Any

from PySide6.QtQml import QJSValue


def from_qml(value: Any) -> Any:
    """
    @brief Unwraps a value crossing the QML->Python boundary into native
    Python types, recursively through nested dicts/lists.

    @details PySide6 marshals a `@Slot("QVariant")` argument built from a
    plain QML JS object literal as a `QJSValue`, not a `dict` — calling
    `dict(value)` on it raises `TypeError` (it isn't iterable the way a real
    dict is). `QJSValue.toVariant()` converts it, and empirically (verified
    with a real `QQmlEngine` round-trip, not assumed from documentation)
    already recurses through nested objects/arrays in current PySide6 — but
    this still recurses manually afterward rather than trust that holds
    forever, since a `QJSValue` surviving inside an otherwise-native
    dict/list is exactly the shape of bug this function exists to close off
    for good (see BOT-061, the local, one-off version of this fix).

    Idempotent: a value that is already native Python (including one this
    function has already unwrapped) passes through unchanged, so call sites
    never need to guard "is this actually a QJSValue" themselves — the one
    thing every `@Slot("QVariant")`/`@Slot("QVariantList")` handler in the
    app should do to its argument before touching it.
    """
    if isinstance(value, QJSValue):
        value = value.toVariant()
    if isinstance(value, dict):
        return {key: from_qml(item) for key, item in value.items()}
    if isinstance(value, list):
        return [from_qml(item) for item in value]
    return value
