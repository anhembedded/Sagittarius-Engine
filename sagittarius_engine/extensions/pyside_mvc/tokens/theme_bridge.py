from PySide6.QtQml import QQmlPropertyMap

from .defaults import with_token_defaults

_THEME_CONTEXT_NAME = "Theme"

_shared_theme_bridge: QQmlPropertyMap | None = None


def get_theme_bridge(palette: dict[str, str] | None = None) -> QQmlPropertyMap:
    """
    @brief Returns the shared theme bridge (lazy singleton) exposing `palette`
    to QML as bindable properties, so `.qml` files reference e.g.
    `Theme.accent` instead of hardcoding hex values per screen.

    @details
    A QQmlPropertyMap rather than a fixed set of named @Property members:
    a property map's keys can be populated from a dict at construction time
    without hand-writing one @Property per token. The vocabulary itself is
    no longer an open question the map is neutral about — required colour
    tokens are engine-owned and validated at `configure_app_qml()` (see
    `tokens.vocabulary`); this function's job is exposure to QML, not
    naming policy.

    One instance app-wide: it holds no per-screen state, and every QML
    context property must point at an object Python keeps alive — a
    module-level singleton makes that ownership unambiguous. Only the
    first caller's palette takes effect; later calls (from subsequent
    screens) just return the already-built instance.

    @param palette Maps QML property name -> color value (typically a hex
    string). Required on the first call; ignored afterwards. Merged with
    every default-backed token category — state, spacing, radius,
    typography, motion (`tokens.defaults.with_token_defaults`, app keys win
    on collision) — so `Theme.stateDisabledOpacity`/`Theme.spaceMd`/etc.
    always resolve to something, even for an app that hasn't opted into
    overriding them yet.
    @raise ValueError If called before any palette has been supplied.
    """
    global _shared_theme_bridge
    if _shared_theme_bridge is None:
        if palette is None:
            raise ValueError(
                "get_theme_bridge() has no palette yet — the first call "
                "(typically from create_quick_widget()) must supply one."
            )
        _shared_theme_bridge = QQmlPropertyMap()
        for key, value in with_token_defaults(palette).items():
            _shared_theme_bridge.insert(key, value)
    return _shared_theme_bridge


def register_theme(quick_widget, palette: dict[str, str] | None = None) -> None:
    """
    @brief Registers the shared theme bridge as the `Theme` context property
    on a QQuickWidget's root context.
    @details Called by QmlHostView before loading any QML source, so every
    screen gets `Theme.*` without repeating the wiring.
    """
    quick_widget.rootContext().setContextProperty(
        _THEME_CONTEXT_NAME, get_theme_bridge(palette)
    )
