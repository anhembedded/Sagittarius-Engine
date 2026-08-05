# PySide6 UI Architecture Rules

This document outlines the strict guidelines for the Presentation Layer (UI) in this project.
The UI is a "dumb plugin" designed with Clean Architecture, CQRS, and Event-Driven Architecture.

## 1. Tối ưu Component (Card)
- **BaseCard Inheritance:** All cards (e.g., `ChartCard`, `ControlCard`, `MonitorCard`) MUST inherit from `BaseCard` (which is a `QFrame`). This ensures a unified layout (`header`, `body`, `footer`) and consistent borders.
- **Global QSS Only:** DO NOT use `setStyleSheet()` inside Python files with hardcoded colors. ALL styling must be moved to `src/presentation/ui/qss/style.qss`. The `MainWindow` will load this file dynamically at startup.

## 2. Tối ưu Screen/View (Dynamic Layouts & Responsiveness)
- **Dynamic Card Generation:** Views should NOT hardcode sets of cards for domains like symbols. Instead, Views must provide methods like `render_symbol_cards(symbols: list[str])` to dynamically instantiate and layout cards (like `ChartCard`).
- **Responsiveness:** Always use `QScrollArea` or `QSplitter` for the main content areas to ensure the UI does not break when resized or when multiple dynamic cards are added.

## 3. Tối ưu Presenter (Signal Mapping & Event Bus)
- **Signal Mapping:** When dealing with dynamic cards, the Presenter MUST loop through the instantiated cards and connect their signals programmatically.
- **Event Bus Boundary:** The Presenter should ONLY listen to Events emitted by the Application Layer (`EventBus`). It MUST NEVER process raw domain logic or database entities directly.
- **Thread Safety:** The Presenter MUST bridge background events to the main UI thread using `PySide6.QtCore.Signal`. Calling UI updates directly from background EventBus threads is strictly PROHIBITED.

## 4. Tối ưu Router (MainWindow & Lazy Loading)
- **Lazy Loading Screens:** Screens MUST NOT be initialized simultaneously at startup. Use `RouterManager` to initialize them on demand when the user navigates to them.
- **Router Isolation:** `MainWindow` delegates all `QStackedWidget` index management and screen initialization to `RouterManager`.
