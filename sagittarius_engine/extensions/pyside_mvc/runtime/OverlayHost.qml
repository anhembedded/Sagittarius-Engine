import QtQuick
import QtQuick.Controls

Item {
    id: root

    // The loaded document owns the modal state.  Python only mirrors that
    // state into QWidget input transparency; it never attempts to count open
    // popups itself because a closePolicy may close one without Python seeing
    // a corresponding call.
    property url contentSource
    readonly property bool hasOpenModal: contentLoader.item !== null
                                       && contentLoader.item.hasOpenModal === true
    readonly property real overlayWidth: overlayBoundsProbe.parent !== null
                                       ? overlayBoundsProbe.parent.width : 0
    readonly property real overlayHeight: overlayBoundsProbe.parent !== null
                                        ? overlayBoundsProbe.parent.height : 0
    readonly property var contentItem: contentLoader.item

    // A Popup is the Qt Quick Controls object that receives Overlay.overlay
    // as its visual parent. It must open once before Controls creates that
    // parent, so the probe is a zero-area, transparent, non-modal popup that
    // has neither visual nor input effects.
    Popup {
        id: overlayBoundsProbe
        closePolicy: Popup.NoAutoClose
        height: 0
        modal: false
        opacity: 0
        visible: true
        width: 0
    }

    Loader {
        id: contentLoader
        anchors.fill: parent
        source: root.contentSource
    }
}
