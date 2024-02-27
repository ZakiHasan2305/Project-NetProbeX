
/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick 6.5
import QtQuick.Controls 6.5
import Test_netprobex_main
import QtQuickUltralite.Layers

Rectangle {
    id: rectangle
    width: 1280
    height: 720

    color: Constants.backgroundColor

    states: [
        State {
            name: "clicked"
        }
    ]
    Image {
        id: image
        x: -15
        y: 0
        width: 1310
        height: 720
        source: "../../../../Downloads/Frame 2 (1).png"
        fillMode: Image.PreserveAspectFit

        Transp_button {
            id: transp_button
            x: 27
            y: 27
            width: 83
            height: 68
        }
    }
}
