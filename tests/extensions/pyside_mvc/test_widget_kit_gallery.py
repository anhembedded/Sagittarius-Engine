"""Sanity coverage for the Widget Kit (EPIC-001C): the Gallery loads clean,
AppDataTable wires columns/model end to end, and the kit's own QML source
carries zero literal colour values — dogfooding the guard EPIC-001B shipped
on the exact surface ui-architecture.md §2.2 targets."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtCore import QObject, QUrl
from PySide6.QtGui import QIcon

from sagittarius_engine.extensions.pyside_mvc.QmlShared import (
    configure_app_qml,
    create_quick_widget,
)
from sagittarius_engine.extensions.pyside_mvc.tokens import (
    REQUIRED_COLOUR_TOKEN_NAMES,
    find_literal_colors,
)

_QML_SHARED_DIR = (
    Path(__file__).resolve().parents[3]
    / "sagittarius_engine"
    / "extensions"
    / "pyside_mvc"
    / "QmlShared"
)
_FIXTURES_DIR = Path(__file__).parent / "fixtures"
_PLACEHOLDER_PALETTE = {name: "#000000" for name in REQUIRED_COLOUR_TOKEN_NAMES}


class _TestIconLoader:
    def get_icon(self, name: str, color: str, size: int) -> QIcon:
        return QIcon()


@pytest.fixture(scope="module", autouse=True)
def configure_qml() -> None:
    configure_app_qml(_PLACEHOLDER_PALETTE, _TestIconLoader(), {})


def test_gallery_loads_with_no_qml_errors(qtbot):
    widget = create_quick_widget()
    qtbot.addWidget(widget)

    widget.setSource(QUrl.fromLocalFile(str(_QML_SHARED_DIR / "Gallery.qml")))

    assert widget.errors() == []
    assert widget.rootObject() is not None


def test_app_data_table_renders_every_row_from_its_model(qtbot):
    widget = create_quick_widget()
    qtbot.addWidget(widget)

    widget.setSource(
        QUrl.fromLocalFile(str(_FIXTURES_DIR / "app_data_table_probe.qml"))
    )

    assert widget.errors() == []
    root = widget.rootObject()
    assert root is not None

    rows_view = root.findChild(QObject, "appDataTableRows")
    assert rows_view is not None
    assert rows_view.property("count") == 2


def test_widget_kit_source_has_zero_literal_colours():
    """The permanent regression test: this exact check already caught 8
    real pre-existing violations in QmlShared when first run (2026-08-22) —
    two legitimate Theme-unavailable fallbacks (now marked token-exempt),
    three with no matching semantic token yet (marked token-exempt with a
    reason), and three genuine drift bugs (fixed to use the matching
    existing token). This test is what keeps the kit at zero going
    forward."""
    findings = find_literal_colors(_QML_SHARED_DIR)

    assert findings == []
