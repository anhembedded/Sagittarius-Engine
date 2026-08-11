import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// Shared button with a standardized enabled/disabled/hover/active visual
// recipe. Promoted out of DevBoardPanel.qml/DatabaseScreen.qml (the
// enabled/disabled/hover part — the same ~6-line background block, plus 2-3
// more `opacity: enabled ? 1.0 : <magic number>` copies per button, was
// reimplemented 7+ times with inconsistent disabled-opacity constants
// 0.4/0.45/0.5/0.6 that didn't even agree with each other within one
// button) and Sidebar.qml's `navButton`/`bottomNavButton` (the `isActive`
// part — those were a second, near-identical ~55-line block each,
// independently typing out the same "selected nav item" tint). `isActive`
// and `enabled` are independent, orthogonal booleans on this one component
// — a button can be selected-but-busy, for instance — rather than two
// separate button types for the two concerns.
//
// Usage:
//     StatefulButton {
//         iconSource: "clock"          // -> image://icons/clock/muted
//         text: "Load History"
//         accentBorder: Theme.border   // or Theme.success / Theme.danger
//         onClicked: viewModel.requestLoadHistory()
//     }
//     StatefulButton {
//         iconSource: modelData.icon
//         text: modelData.label
//         iconSize: 18
//         fontSize: 13
//         accentBorder: Theme.stateNavBorder
//         isActive: modelData.route === viewModel.activeRoute
//         onClicked: viewModel.navigate(modelData.route)
//     }
Button {
    id: root

    //: Icon name only (no color suffix) — resolved against the app's
    //: `image://icons/<name>/<iconTint>` provider. Empty string omits the
    //: icon.
    property string iconSource: ""
    //: Icon color token. Defaults to the same active/inactive split as the
    //: text/border (muted when idle, accent when isActive) — override with
    //: a semantic token (e.g. "success"/"danger") for an action button
    //: whose icon color doesn't depend on selection state (Start/Stop).
    property string iconTint: root.isActive ? "accent" : "muted"
    //: Border color while NOT active — pass a semantic token
    //: (Theme.success/Theme.danger/Theme.stateNavBorder) for an
    //: affirmative/destructive/nav-item look, or leave the Theme.border
    //: default for a neutral one. Ignored while isActive is true
    //: (Theme.accent takes over).
    property color accentBorder: Theme.border
    property int iconSize: 13
    property int fontSize: 11
    property int contentSpacing: 5
    //: Marks this button as the current selection (e.g. the active nav
    //: route) — independent of enabled/disabled.
    property bool isActive: false
    //: Off by default (matches every action button's compact, icon+text
    //: centered-as-a-group look). Turn on for a fixed-width container where
    //: a long label needs to truncate instead of overflowing (e.g. a nav
    //: sidebar item) — makes the text fill the remaining row width and
    //: elide, instead of sizing to its own content.
    property bool textFillWidth: false

    implicitHeight: 32

    contentItem: RowLayout {
        spacing: root.contentSpacing

        Image {
            visible: root.iconSource !== ""
            source: root.iconSource === "" ? "" : "image://icons/" + root.iconSource + "/" + root.iconTint
            sourceSize.width: root.iconSize
            sourceSize.height: root.iconSize
            Layout.preferredWidth: root.iconSize
            Layout.preferredHeight: root.iconSize
            opacity: root.enabled ? 1.0 : Theme.stateDisabledOpacity
        }

        Text {
            text: root.text
            color: root.isActive ? Theme.accent : Theme.textPrimary
            font.pixelSize: root.fontSize
            opacity: root.enabled ? 1.0 : Theme.stateDisabledOpacity
            Layout.fillWidth: root.textFillWidth
            elide: root.textFillWidth ? Text.ElideRight : Text.ElideNone
        }
    }

    background: Rectangle {
        implicitHeight: root.implicitHeight
        radius: 6
        color: root.isActive
               ? Theme.stateActiveTint
               : (root.hovered && root.enabled ? Theme.stateHoverBg : Theme.stateIdleBg)
        border.color: root.isActive ? Theme.accent : root.accentBorder
        border.width: 1
        opacity: root.enabled ? 1.0 : Theme.stateDisabledOpacity
    }
}
