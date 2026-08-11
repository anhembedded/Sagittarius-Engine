1. *Add visual focus indicators to QML UI components for keyboard accessibility.*
   - In `Sidebar.qml`, add a visible focus state to the navigation buttons.
   - In `LogPanel.qml`, add a focus indicator for the "Clear" button.
   - Update `FieldBackground` (in `DevBoardPanel.qml` and `DatabaseScreen.qml`) to show a focus border.
2. *Document the UX learning in `.jules/palette.md`.*
   - Note the pattern of adding keyboard focus styles using the `visualFocus` property in QtQuick Controls.
3. *Complete pre commit steps.*
   - Ensure tests pass and standard checks are completed.
4. *Submit PR with the micro-UX improvement.*
   - Submit the change with clear UX benefits (keyboard navigation).
