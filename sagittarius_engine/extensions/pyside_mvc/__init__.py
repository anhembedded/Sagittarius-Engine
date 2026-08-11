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
    from .ui_matrix_mixin import UIMatrixMixin
    from .thread_bridge import safe_ui_action
    from .QmlShared import (
        ICON_PROVIDER_ID,
        AppQmlConfig,
        BaseQmlViewModel,
        DEFAULT_STATE_TOKENS,
        IconImageProvider,
        IIconLoader,
        LogListModel,
        QmlHostView,
        configure_app_qml,
        create_quick_widget,
        ensure_qml_style,
        get_theme_bridge,
        register_theme,
        with_state_token_defaults,
    )

    __all__ = [
        "ICON_PROVIDER_ID",
        "AppQmlConfig",
        "BasePresenter",
        "BaseQmlViewModel",
        "BaseView",
        "DEFAULT_STATE_TOKENS",
        "IconImageProvider",
        "IIconLoader",
        "LogListModel",
        "PresenterManager",
        "QmlHostView",
        "UIMatrixMixin",
        "configure_app_qml",
        "create_quick_widget",
        "ensure_qml_style",
        "get_theme_bridge",
        "register_theme",
        "safe_ui_action",
        "with_state_token_defaults",
    ]
