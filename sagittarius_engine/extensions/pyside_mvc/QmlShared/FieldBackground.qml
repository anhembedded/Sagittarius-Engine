import QtQuick

// Shared field background (promoted from DevBoardPanel.qml/DatabaseScreen.qml,
// which each used to define this as an identical local `component` block).
// Usage: `background: FieldBackground {}` on any ComboBox/TextField.
Rectangle {
    color: Theme && Theme.stateIdleBg ? Theme.stateIdleBg : "#181a24"
    border.color: Theme && Theme.border ? Theme.border : "#2a2d3d"
    border.width: 1
    radius: 6
    implicitHeight: 32
}
