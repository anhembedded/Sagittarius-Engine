import functools
import traceback
from collections.abc import Callable
from typing import Any

from ..mvc.base_view import DEV_MODE_CONFIG_KEY
from .ui_action_events import UiActionFailedEvent


def safe_ui_action(func: Callable) -> Callable:
    """
    @brief Decorator to catch exceptions in Qt Slots safely.
    @details
    When an exception occurs in a PySide6 Slot (especially one triggered from a background thread
    via an EventBus), it can silently crash the application or freeze the UI without a clear traceback.
    This decorator ensures exceptions are caught and do not propagate up to the Qt event loop — but
    the failure is never silent: it's logged with a full traceback, emitted as a structured
    `UiActionFailedEvent` (so tests/monitoring can observe it instead of scraping stdout), and — when
    the app's `dev.mode` config flag (`DEV_MODE_CONFIG_KEY`) is on — re-raised, so a caught exception
    always fails loud during development instead of only reaching production users silently (BOT-066,
    see BOT-061 for the real bug this used to hide).

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
            tb = traceback.format_exc()
            owner = args[0] if args else None

            logger = getattr(owner, "logger", None)
            if logger is not None:
                logger.error(
                    f"[UI Thread Bridge Error] Exception in {func.__name__}: {e}",
                    extra={"traceback": tb},
                )
            else:
                # No BasePresenter/ILogger to hand this to (e.g. a bare
                # function outside the presenter layer) — stdout is the
                # only place left, so include the traceback here too.
                print(
                    f"[UI Thread Bridge Error] Exception in {func.__name__}: {e}\n{tb}"
                )

            # Duck typing: If the object (args[0] = self) has a ui_log_signal, emit the error there too
            if owner is not None and hasattr(owner, "ui_log_signal"):
                owner.ui_log_signal.emit(f"{func.__name__} failed: {e}")

            event_bus = getattr(owner, "event_bus", None)
            if event_bus is not None:
                event_bus.emit(
                    UiActionFailedEvent(
                        function_name=func.__name__,
                        exception_type=type(e).__name__,
                        message=str(e),
                        traceback=tb,
                    )
                )

            config = getattr(owner, "config", None)
            if config is not None and config.get(DEV_MODE_CONFIG_KEY, False):
                raise

            return None

    return wrapper
