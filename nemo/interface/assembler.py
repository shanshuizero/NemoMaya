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
import maya.OpenMayaUI as omui
from maya import cmds

import os
import glob
import sys

import Qt
import dayu_widgets


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major == 2:
        return Qt.QtCompat.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)
    else:
        return Qt.QtCompat.wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class WidgetNemoAssembler(QtWidgets.QWidget):
    symbol_unknown = "<Unknown>"

    def __init__(self, parent=maya_main_window()):
        super(WidgetNemoAssembler, self).__init__()
        self.setParent(parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("Nemo Assembler")
        self.layout = self.create_ui()
        self.setLayout(self.layout)

    def dll_mode(self):
        return self.options_runtime.isChecked()

    def create_ui(self):
        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(self.create_version())

        layout_name = QtWidgets.QHBoxLayout()
        label_head = dayu_widgets.MLabel(text="Name:")
        label_head.setAlignment(QtCore.Qt.ElideLeft)
        label_head.setFixedWidth(60)
        layout_name.addWidget(label_head)
        self.label_name = dayu_widgets.MLabel(text=WidgetNemoAssembler.symbol_unknown)
        self.label_name.setAlignment(QtCore.Qt.AlignCenter)
        layout_name.addWidget(self.label_name)
        layout.addLayout(layout_name)

        layout_receive = QtWidgets.QHBoxLayout()
        layout_receive.addWidget(dayu_widgets.MLabel("Receive:"))
        self.browser_dir_receive = dayu_widgets.MClickBrowserFolderToolButton()
        layout_receive.addWidget(self.browser_dir_receive)
        label_receive = dayu_widgets.MLabel("<Select Folder>")
        label_receive.set_elide_mode(QtCore.Qt.ElideLeft)
        layout_receive.addWidget(label_receive)
        self.browser_dir_receive.sig_folder_changed.connect(label_receive.setText)
        self.browser_dir_receive.sig_folder_changed.connect(self.on_select_receive_folder)
        layout.addLayout(layout_receive)

        layout_upload = QtWidgets.QHBoxLayout()
        layout_upload.addWidget(dayu_widgets.MLabel("Export: "))
        self.browser_dir_upload = dayu_widgets.MClickBrowserFolderToolButton()
        layout_upload.addWidget(self.browser_dir_upload)
        self.label_upload = dayu_widgets.MLabel("<Select Folder>")
        self.label_upload.set_elide_mode(QtCore.Qt.ElideLeft)
        layout_upload.addWidget(self.label_upload)
        self.browser_dir_upload.sig_folder_changed.connect(self.on_select_upload_folder)
        layout.addLayout(layout_upload)

        layout_output = QtWidgets.QHBoxLayout()
        layout_output.addWidget(dayu_widgets.MLabel("Runtime:"))
        self.browser_dir_output = dayu_widgets.MClickBrowserFolderToolButton()
        layout_output.addWidget(self.browser_dir_output)
        self.label_output = dayu_widgets.MLabel("<Select Folder>")
        self.label_output.set_elide_mode(QtCore.Qt.ElideLeft)
        layout_output.addWidget(self.label_output)
        self.browser_dir_output.sig_folder_changed.connect(self.on_select_output_folder)
        layout.addLayout(layout_output)

        layout_options = QtWidgets.QHBoxLayout()
        self.options_runtime = dayu_widgets.MCheckBox("runtime")
        if "win32" == sys.platform:
            self.options_runtime.setEnabled(False)
        layout_options.addWidget(self.options_runtime)
        self.options_relative = dayu_widgets.MCheckBox("relative")
        layout_options.addWidget(self.options_relative)
        layout.addLayout(layout_options)

        btn_assemble = dayu_widgets.MPushButton("Assemble")
        btn_assemble.clicked.connect(self.on_assemble)
        layout.addWidget(btn_assemble)
        return layout

    @staticmethod
    def ext(dll_mode):
        if dll_mode:
            return "dll" if "win32" == sys.platform else "so"
        else:
            return "mll" if "win32" == sys.platform else "so"

    @staticmethod
    def binary_name(identifier, dll_mode):
        if dll_mode:
            return "{}.dll".format(identifier) if "win32" == sys.platform else "lib{}.so".format(identifier)
        else:
            return "{}.{}".format(identifier, WidgetNemoAssembler.ext(dll_mode))

    def on_select_receive_folder(self, path):
        try:
            binary = glob.glob('{}/*.{}'.format(path, WidgetNemoAssembler.ext(self.dll_mode())))
            if "win32" == sys.platform and not binary and glob.glob('{}/*.{}'.format(path, WidgetNemoAssembler.ext(not self.dll_mode()))):
                self.options_runtime.setChecked(not self.dll_mode())
                binary = glob.glob('{}/*.{}'.format(path, WidgetNemoAssembler.ext(self.dll_mode())))
            binary = binary[0]

            name = os.path.splitext(os.path.basename(binary))[0]
            if "win32" != sys.platform and name.startswith("lib"):
                name = name[3:]
                self.options_runtime.setChecked(True)

            self.label_name.setText(name)
        except Exception as e:
            self.label_name.setText(WidgetNemoAssembler.symbol_unknown)

    def on_select_upload_folder(self, path):
        if path is None:
            return
        if path == self.browser_dir_output.dayu_path:
            QMessageBox.critical(self, "Error", "Export folder cannot be the same with Output folder")
            return
        self.label_upload.setText(path)

    def on_select_output_folder(self, path):
        if path is None:
            return
        if path == self.browser_dir_upload.dayu_path:
            QMessageBox.critical(self, "Error", "Output folder cannot be the same with Export folder")
            return
        self.label_output.setText(path)

    def on_assemble(self):
        name = self.label_name.text()
        if name == WidgetNemoAssembler.symbol_unknown:
            QMessageBox.critical(self, "Error", "Select Receive folder containing correct binary.")
            return

        dir_receive = str(self.browser_dir_receive.dayu_path)
        path_config = "{}/{}__CONFIG.json".format(dir_receive, name)
        path_bin = "{}/{}".format(dir_receive, WidgetNemoAssembler.binary_name(name, self.dll_mode()))
        dir_upload = str(self.browser_dir_upload.dayu_path)
        path_resource = "{}/{}__RESOURCE.nemodata".format(dir_upload, name)
        path_scene = "{}/{}__SCENE.json".format(dir_upload, name)
        path_shading = "{}/{}__MAT.json".format(dir_upload, name)
        path_materials = "{}/{}__MAT.ma".format(dir_upload, name)

        def clone(path, dir_to):
            new_path = "{}/{}".format(dir_to, os.path.basename(path))
            shutil.copy(path, new_path)
            return new_path

        import shutil
        try:
            dir_output = str(self.browser_dir_output.dayu_path)
            if os.listdir(dir_output):
                if QMessageBox.StandardButton.No == QMessageBox.question(self, "Export folder not empty",
                                                                         "Do you really want to overwrite {}?".format(dir_output)):
                    return
            path_resource = clone(path_resource, dir_output)
            path_bin = clone(path_bin, dir_output)
            if self.dll_mode():
                path_config = clone(path_config, dir_output)
                path_shading = clone(path_shading, dir_output)

            from nemo.n2m import n2m
            if self.dll_mode():
                cmds.file(path_materials, o=True, f=True)
            else:
                cmds.file(new=True, f=True)
            n2m.assemble(path_config, path_scene, path_bin, path_resource, path_shading, name, self.dll_mode(), relative_path=self.options_relative.isChecked())
            cmds.file(rename='{}/{}.ma'.format(dir_output, name))
            cmds.file(save=True, type="mayaAscii")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def create_version(self):
        timestamp = "<unknown>"
        try:
            import NemoMaya
            timestamp = NemoMaya.get_timestamp()
        except:
            pass
        return dayu_widgets.MLabel("Timestamp: {}".format(timestamp))


def show():
    widget = WidgetNemoAssembler()
    from dayu_widgets import dayu_theme
    dayu_theme.apply(widget)
    widget.show()


if __name__ == "__main__":
    show()
