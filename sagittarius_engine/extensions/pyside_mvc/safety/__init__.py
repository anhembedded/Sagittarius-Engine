"""
@brief Thread-safety and crash-visibility guardrails — cross-thread UI
mutation detection, the `safe_ui_action` exception boundary, Qt
signal/crash handling, and the legacy `ui_matrix.json`-reflection mixin
`QmlHostView`/`BaseQmlViewModel` are superseding. Split out of the flat
top-level `pyside_mvc/` (EPIC-001C reorg) as one coherent "keep the UI
thread alive and observable" concern.
"""

from .thread_affinity import (
    CrossThreadUiMutationError,
    not_a_ui_mutator,
    set_thread_affinity_dev_mode,
    ui_mutator,
    unprotected_mutators,
)
from .thread_bridge import safe_ui_action
from .ui_action_events import UiActionFailedEvent
from .ui_matrix_mixin import UIMatrixMixin
from .ui_watchdog import UIWatchdog, setup_qt_signal_handling

__all__ = [
    "CrossThreadUiMutationError",
    "UIMatrixMixin",
    "UIWatchdog",
    "UiActionFailedEvent",
    "not_a_ui_mutator",
    "safe_ui_action",
    "set_thread_affinity_dev_mode",
    "setup_qt_signal_handling",
    "ui_mutator",
    "unprotected_mutators",
]
