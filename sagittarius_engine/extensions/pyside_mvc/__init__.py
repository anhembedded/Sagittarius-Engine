"""
@brief PySide6 MVC Extension for Sagittarius Engine.
@details Provides true lazy-loaded UI routing, base presenters, and data-driven matrix UI.
"""

import sys

# Dependency Guard: Protects the UI-Agnostic Core from crashing if PySide6 is missing.
try:
    import PySide6
except ImportError:
    print(
        "[sagittarius_engine.extensions.pyside_mvc] WARNING: PySide6 is not installed. "
        "The pyside_mvc extension will be unavailable. Please install PySide6 if you need GUI features.",
        file=sys.stderr,
    )
    # Expose dummies or just let subsequent imports fail explicitly when consumer code runs.
    # We don't raise an error here because simply scanning the extensions folder shouldn't crash the engine.
else:
    from .base_presenter import BasePresenter
    from .base_view import BaseView
    from .presenter_manager import PresenterManager
    from .QmlShared import (
        DEFAULT_STATE_TOKENS,
        ICON_PROVIDER_ID,
        AppQmlConfig,
        BaseQmlViewModel,
        IconImageProvider,
        IIconLoader,
        LogListModel,
        OverlayHost,
        QmlHostView,
        configure_app_qml,
        create_quick_widget,
        ensure_qml_style,
        from_qml,
        get_theme_bridge,
        register_theme,
        with_state_token_defaults,
    )
    from .thread_affinity import (
        CrossThreadUiMutationError,
        not_a_ui_mutator,
        set_thread_affinity_dev_mode,
        ui_mutator,
        unprotected_mutators,
    )
    from .thread_bridge import safe_ui_action
    from .tokens import (
        DEFAULT_MOTION_TOKENS,
        DEFAULT_RADIUS_TOKENS,
        DEFAULT_SPACING_TOKENS,
        DEFAULT_TYPOGRAPHY_TOKENS,
        REQUIRED_COLOUR_TOKEN_NAMES,
        REQUIRED_COLOUR_TOKENS,
        LiteralColorFinding,
        MissingRequiredTokensError,
        TokenSpec,
        find_literal_colors,
        missing_required_tokens,
        with_token_defaults,
    )
    from .ui_matrix_mixin import UIMatrixMixin
    from .ui_watchdog import UIWatchdog, setup_qt_signal_handling

    __all__ = [
        "DEFAULT_MOTION_TOKENS",
        "DEFAULT_RADIUS_TOKENS",
        "DEFAULT_SPACING_TOKENS",
        "DEFAULT_STATE_TOKENS",
        "DEFAULT_TYPOGRAPHY_TOKENS",
        "ICON_PROVIDER_ID",
        "REQUIRED_COLOUR_TOKENS",
        "REQUIRED_COLOUR_TOKEN_NAMES",
        "AppQmlConfig",
        "BasePresenter",
        "BaseQmlViewModel",
        "BaseView",
        "CrossThreadUiMutationError",
        "IIconLoader",
        "IconImageProvider",
        "LiteralColorFinding",
        "LogListModel",
        "MissingRequiredTokensError",
        "OverlayHost",
        "PresenterManager",
        "QmlHostView",
        "TokenSpec",
        "UIMatrixMixin",
        "UIWatchdog",
        "configure_app_qml",
        "create_quick_widget",
        "ensure_qml_style",
        "find_literal_colors",
        "from_qml",
        "get_theme_bridge",
        "missing_required_tokens",
        "not_a_ui_mutator",
        "register_theme",
        "safe_ui_action",
        "set_thread_affinity_dev_mode",
        "setup_qt_signal_handling",
        "ui_mutator",
        "unprotected_mutators",
        "with_state_token_defaults",
        "with_token_defaults",
    ]
