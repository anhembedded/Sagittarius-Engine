from sagittarius_engine.extensions.pyside_mvc.QmlShared.state_tokens import (
    DEFAULT_STATE_TOKENS,
    with_state_token_defaults,
)


def test_with_state_token_defaults_returns_engine_defaults_when_palette_is_none():
    assert with_state_token_defaults(None) == DEFAULT_STATE_TOKENS


def test_with_state_token_defaults_returns_engine_defaults_for_an_empty_palette():
    assert with_state_token_defaults({}) == DEFAULT_STATE_TOKENS


def test_with_state_token_defaults_lets_app_values_override_matching_keys():
    app_palette = {"stateIdleBg": "#17181d", "stateHoverBg": "#1f2127"}

    merged = with_state_token_defaults(app_palette)

    assert merged["stateIdleBg"] == "#17181d"
    assert merged["stateHoverBg"] == "#1f2127"
    # Keys the app didn't override still fall back to the engine default.
    assert merged["stateDisabledOpacity"] == DEFAULT_STATE_TOKENS["stateDisabledOpacity"]
    assert merged["stateActiveTint"] == DEFAULT_STATE_TOKENS["stateActiveTint"]
    assert merged["stateNavBorder"] == DEFAULT_STATE_TOKENS["stateNavBorder"]


def test_with_state_token_defaults_preserves_unrelated_app_keys():
    """An app's full palette dict (accent/bgCard/etc.) passes through
    untouched alongside the state tokens — this isn't a filter, it's a
    gap-fill merge."""
    app_palette = {"accent": "#F3BA2F", "bgCard": "#111318"}

    merged = with_state_token_defaults(app_palette)

    assert merged["accent"] == "#F3BA2F"
    assert merged["bgCard"] == "#111318"
    assert merged["stateIdleBg"] == DEFAULT_STATE_TOKENS["stateIdleBg"]


def test_with_state_token_defaults_does_not_mutate_its_inputs():
    app_palette = {"accent": "#F3BA2F"}
    original_defaults = dict(DEFAULT_STATE_TOKENS)
    original_app_palette = dict(app_palette)

    with_state_token_defaults(app_palette)

    assert DEFAULT_STATE_TOKENS == original_defaults
    assert app_palette == original_app_palette
