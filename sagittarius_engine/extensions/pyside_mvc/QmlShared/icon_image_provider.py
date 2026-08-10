from typing import Protocol

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtQuick import QQuickImageProvider

ICON_PROVIDER_ID = "icons"

_DEFAULT_SIZE = 20
_HEX_LENGTH = 6
_FALLBACK_COLOR = "#848E9C"


class IIconLoader(Protocol):
    """@brief Port an app's own icon loader must satisfy to back
    IconImageProvider — see e.g. Binace_Bot's assets/icon_loader.py."""

    def get_icon(self, name: str, color: str, size: int) -> QIcon: ...


class IconImageProvider(QQuickImageProvider):
    """
    @brief Serves recolored icons to QML via `image://icons/<name>/<color>`.

    @details
    QML has no equivalent of QIcon, and SVG icon sets that use a
    `currentColor`-style placeholder need a real recoloring step a plain
    `Image { source: "...svg" }` can't do. This adapter delegates to an
    app-supplied `IIconLoader` so recoloring/caching/blank-icon-fallback
    stay wherever the app already implements them, rather than being
    reimplemented here — the engine only owns the QML image-provider glue
    and the `name/color` URL parsing.

    `<color>` is either a key in the app-supplied `icon_palette` or a raw
    6-digit hex without the leading '#' (QML URLs cannot carry '#').
    Unknown values fall back to `_FALLBACK_COLOR`.
    """

    def __init__(self, icon_loader: IIconLoader, icon_palette: dict[str, str]) -> None:
        super().__init__(QQuickImageProvider.ImageType.Pixmap)
        self._icon_loader = icon_loader
        self._icon_palette = icon_palette

    def requestPixmap(
        self, image_id: str, size: QSize, requested_size: QSize
    ) -> QPixmap:
        """
        @param image_id The URL path after `image://icons/`, i.e. "name" or
        "name/color".
        @param size Out-parameter Qt fills with the produced size.
        @param requested_size QML's `sourceSize`, or an invalid size when the
        caller didn't constrain it.
        """
        name, color = self._parse_id(image_id)
        edge = self._resolve_edge(requested_size)

        pixmap = self._icon_loader.get_icon(name, color, edge).pixmap(edge, edge)
        size.setWidth(pixmap.width())
        size.setHeight(pixmap.height())
        return pixmap

    def _parse_id(self, image_id: str) -> tuple[str, str]:
        name, _, color_token = image_id.partition("/")
        return name, self._resolve_color(color_token)

    def _resolve_color(self, token: str) -> str:
        if not token:
            return self._icon_palette.get("muted", _FALLBACK_COLOR)
        named = self._icon_palette.get(token.lower())
        if named is not None:
            return named
        if len(token) == _HEX_LENGTH:
            try:
                int(token, 16)
            except ValueError:
                return self._icon_palette.get("muted", _FALLBACK_COLOR)
            return f"#{token}"
        return self._icon_palette.get("muted", _FALLBACK_COLOR)

    @staticmethod
    def _resolve_edge(requested_size: QSize) -> int:
        """Icons are square: takes the larger requested dimension, or the
        default when QML didn't specify a sourceSize."""
        edge = max(requested_size.width(), requested_size.height())
        return edge if edge > 0 else _DEFAULT_SIZE
