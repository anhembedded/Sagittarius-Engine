"""
@brief The UI Engine's design-token layer — the engine's fixed semantic
token vocabulary, its bootstrap-time completeness validation, and the
anti-literal QML guard that keeps a consuming app off raw visual values.
See `ui-architecture.md` and `Tasks/epics/EPIC-001_ui_engine_foundation/`.
"""

from .defaults import (
    DEFAULT_MOTION_TOKENS,
    DEFAULT_RADIUS_TOKENS,
    DEFAULT_SPACING_TOKENS,
    DEFAULT_TYPOGRAPHY_TOKENS,
    with_token_defaults,
)
from .qml_literal_guard import LiteralColorFinding, find_literal_colors
from .vocabulary import (
    REQUIRED_COLOUR_TOKEN_NAMES,
    REQUIRED_COLOUR_TOKENS,
    MissingRequiredTokensError,
    TokenSpec,
    missing_required_tokens,
)

__all__ = [
    "DEFAULT_MOTION_TOKENS",
    "DEFAULT_RADIUS_TOKENS",
    "DEFAULT_SPACING_TOKENS",
    "DEFAULT_TYPOGRAPHY_TOKENS",
    "REQUIRED_COLOUR_TOKENS",
    "REQUIRED_COLOUR_TOKEN_NAMES",
    "LiteralColorFinding",
    "MissingRequiredTokensError",
    "TokenSpec",
    "find_literal_colors",
    "missing_required_tokens",
    "with_token_defaults",
]
