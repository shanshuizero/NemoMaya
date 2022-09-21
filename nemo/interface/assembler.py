"""
 Copyright (c) 2022 OctMedia

 Permission is hereby granted, free of charge, to any person obtaining a copy of
 this software and associated documentation files (the "Software"), to deal in
 the Software without restriction, including without limitation the rights to
 use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 the Software, and to permit persons to whom the Software is furnished to do so,
 subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 """

from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QMessageBox

import Qt
import dayu_widgets


def maya_main_window():
    import maya.OpenMayaUI as omui
    import sys
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major == 2:
        return Qt.QtCompat.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)
    else:
        return Qt.QtCompat.wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class WidgetNemoAssembler(QtWidgets.QWidget):

    def __init__(self, parent=maya_main_window()):
        super(WidgetNemoAssembler, self).__init__()
        self.setParent(parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("Nemo Assembler")
        self.layout = self.create_ui()
        self.setLayout(self.layout)

    def create_ui(self):
        layout = QtWidgets.QVBoxLayout()

        layout_export = QtWidgets.QHBoxLayout()
        layout_export.addWidget(dayu_widgets.MLabel("Export: "))
        self.browser_zip_export = dayu_widgets.MClickBrowserFileToolButton()
        layout_export.addWidget(self.browser_zip_export)
        label_export = dayu_widgets.MLabel("<Select Exported Zip>")
        label_export.set_elide_mode(QtCore.Qt.ElideLeft)
        layout_export.addWidget(label_export)
        self.browser_zip_export.set_dayu_filters([".zip"])
        self.browser_zip_export.sig_file_changed.connect(label_export.setText)
        layout.addLayout(layout_export)

        layout_binary = QtWidgets.QHBoxLayout()
        layout_binary.addWidget(dayu_widgets.MLabel("Binary:"))
        self.browser_zip_binary = dayu_widgets.MClickBrowserFileToolButton()
        layout_binary.addWidget(self.browser_zip_binary)
        label_binary = dayu_widgets.MLabel("<Select Received Zip>")
        label_binary.set_elide_mode(QtCore.Qt.ElideLeft)
        layout_binary.addWidget(label_binary)
        self.browser_zip_binary.set_dayu_filters([".zip"])
        self.browser_zip_binary.sig_file_changed.connect(label_binary.setText)
        layout.addLayout(layout_binary)

        layout_output = QtWidgets.QHBoxLayout()
        layout_output.addWidget(dayu_widgets.MLabel("Runtime:"))
        self.browser_dir_output = dayu_widgets.MClickBrowserFolderToolButton()
        layout_output.addWidget(self.browser_dir_output)
        label_output = dayu_widgets.MLabel("<Select Output Path>")
        label_output.set_elide_mode(QtCore.Qt.ElideLeft)
        layout_output.addWidget(label_output)
        self.browser_dir_output.sig_folder_changed.connect(label_output.setText)
        layout.addLayout(layout_output)

        layout_options = QtWidgets.QHBoxLayout()
        self.options_relative = dayu_widgets.MCheckBox("relative")
        self.options_relative.setChecked(True)
        layout_options.addWidget(self.options_relative)
        layout.addLayout(layout_options)

        btn_assemble = dayu_widgets.MPushButton("Assemble")
        btn_assemble.clicked.connect(self.on_assemble)
        layout.addWidget(btn_assemble)
        return layout

    def on_assemble(self):
        try:
            from nemo.n2m import n2m
            n2m.assemble(str(self.browser_zip_export.dayu_path),
                         str(self.browser_zip_binary.dayu_path),
                         str(self.browser_dir_output.dayu_path),
                         relative_path=self.options_relative.isChecked())
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


def show():
    widget = WidgetNemoAssembler()
    from dayu_widgets import dayu_theme
    dayu_theme.apply(widget)
    widget.show()


if __name__ == "__main__":
    show()
