import QtQuick
import QtQuick.Controls

Item {
    id: root

    property bool hasOpenModal: false
    property string suppliedLabel: typeof overlayLabel === "undefined" ? "" : overlayLabel

    Popup {
        id: modal
        closePolicy: Popup.NoAutoClose
        height: 240
        modal: true
        opacity: 1
        visible: root.hasOpenModal
        width: 360
        x: (Overlay.overlay.width - width) / 2
        y: (Overlay.overlay.height - height) / 2

        background: Rectangle {
            color: "#1A365D"
        }
    }
}
