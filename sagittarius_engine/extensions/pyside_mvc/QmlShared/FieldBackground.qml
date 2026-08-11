import QtQuick

// Shared field background (promoted from DevBoardPanel.qml/DatabaseScreen.qml,
// which each used to define this as an identical local `component` block).
// Usage: `background: FieldBackground {}` on any ComboBox/TextField.
Rectangle {
    color: Theme.stateIdleBg
    border.color: Theme.border
    border.width: 1
    radius: 6
    implicitHeight: 32
}
