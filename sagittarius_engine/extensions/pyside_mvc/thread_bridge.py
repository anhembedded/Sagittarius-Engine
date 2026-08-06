import functools
from collections.abc import Callable
from typing import Any

from PySide6.QtCore import QObject


def safe_ui_action(func: Callable) -> Callable:
    """
    @brief Decorator to catch exceptions in Qt Slots safely.
    @details
    When an exception occurs in a PySide6 Slot (especially one triggered from a background thread
    via an EventBus), it can silently crash the application or freeze the UI without a clear traceback.
    This decorator ensures exceptions are caught, printed, and do not propagate up to the Qt event loop.
    
    Usage:
        @Slot()
        @safe_ui_action
        def on_button_clicked(self):
            ...
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # We use string formatting since this is UI-agnostic and might not have a logger
            print(f"[UI Thread Bridge Error] Exception in {func.__name__}: {e}")
            
            # Duck typing: If the object (args[0] = self) has a ui_log_signal, emit the error there too
            if args and hasattr(args[0], "ui_log_signal"):
                args[0].ui_log_signal.emit(f"{func.__name__} failed: {e}")
                
            # Could emit a generic signal here if needed, but for now we just swallow to prevent crash

    return wrapper
