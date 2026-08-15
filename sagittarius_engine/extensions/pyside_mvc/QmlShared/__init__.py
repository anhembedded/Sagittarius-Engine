"""
@brief Shared QML application infrastructure: theme bridge, icon provider,
a base ViewModel carrying FSM state, and a reusable LogPanel.qml component.

@details
Promoted out of a single consuming app once a second real QML consumer
needed the same plumbing — see AppQmlConfig/configure_app_qml for the one
piece every app must wire up before constructing any QmlHostView.
"""

from .base_view_model import BaseQmlViewModel
from .icon_image_provider import ICON_PROVIDER_ID, IconImageProvider, IIconLoader
from .log_list_model import LogListModel
from .overlay_host import OverlayHost
from .qml_host_view import (
    AppQmlConfig,
    QmlHostView,
    configure_app_qml,
    create_quick_widget,
)
from .qml_style import ensure_qml_style
from .qml_value_normalizer import from_qml
from .state_tokens import DEFAULT_STATE_TOKENS, with_state_token_defaults
from .theme_bridge import get_theme_bridge, register_theme

__all__ = [
    "DEFAULT_STATE_TOKENS",
    "ICON_PROVIDER_ID",
    "AppQmlConfig",
    "BaseQmlViewModel",
    "IIconLoader",
    "IconImageProvider",
    "LogListModel",
    "OverlayHost",
    "QmlHostView",
    "configure_app_qml",
    "create_quick_widget",
    "ensure_qml_style",
    "from_qml",
    "get_theme_bridge",
    "register_theme",
    "with_state_token_defaults",
]
