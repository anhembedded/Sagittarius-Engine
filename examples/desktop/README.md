# Desktop Reference Application

This reference application validates integration with event-driven desktop architectures (such as PySide6, PyQt6, or Tkinter).

## Key Patterns
- **Engine First**: The engine boots successfully before any UI components are created.
- **Responsive UI Thread**: Heavy/I/O calculations are delegated to the engine `TaskManager`.
- **UI-Safe Event Updates**: Worker threads notify the UI thread of status changes thread-safely via EventBus events.
