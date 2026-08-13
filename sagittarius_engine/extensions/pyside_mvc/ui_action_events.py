from dataclasses import dataclass


@dataclass(frozen=True)
class UiActionFailedEvent:
    """
    @brief Emitted by `safe_ui_action` whenever it catches an exception.
    @details Exists so a caught-and-swallowed UI-thread error becomes
    observable and testable instead of only reaching stdout/a best-effort
    duck-typed log signal — subscribe via `event_bus.on(UiActionFailedEvent,
    handler)` rather than capturing stdout. `traceback` is the full
    `traceback.format_exc()` text, not just `str(exception)` — a bare
    message previously cost a misdirected investigation (see BOT-061).
    """

    function_name: str
    exception_type: str
    message: str
    traceback: str
