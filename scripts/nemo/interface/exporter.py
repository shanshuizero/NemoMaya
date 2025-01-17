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

from __future__ import print_function
from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QMessageBox
import maya.OpenMayaUI as omui
from maya import cmds

import os
import json

import Qt
import dayu_widgets


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    import sys
    if sys.version_info.major == 2:
        return Qt.QtCompat.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)
    else:
        return Qt.QtCompat.wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class WidgetNemoExporter(QtWidgets.QWidget):

    def __init__(self, parent=maya_main_window()):
        super(WidgetNemoExporter, self).__init__()
        self.setParent(parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("Nemo Exporter v{}".format(WidgetNemoExporter.get_version()))
        self.layout = self.create_ui()
        self.setLayout(self.layout)
        cmds.select(cl=True)

        if cmds.optionVar(exists='NEMO_EXPORT_CONFIG'):
            self.load_config(json.loads(cmds.optionVar(q='NEMO_EXPORT_CONFIG')))
        else:
            self.load_config(dict())

    def create_ui(self):
        main_layout = QtWidgets.QVBoxLayout()

        main_layout.addLayout(self.create_controllers())
        main_layout.addLayout(self.create_shapes())
        main_layout.addLayout(self.create_export())
        main_layout.addStretch()
        return main_layout

    def check(self):
        from nemo import utils

        for x in cmds.ls(type='transform') + cmds.ls(type='joint'):
            s = cmds.getAttr('{}.scale'.format(x))[0]
            if abs(s[0]) < 1E-5 or abs(s[1]) < 1E-5 or abs(s[2]) < 1E-5:
                raise RuntimeError("zero scale is not allowed:\n\t{}.scale is {}".format(x, s))

        if not utils.get_root():
            raise RuntimeError("Should have exactly one top node in hierarchy")

    @staticmethod
    def get_version():
        try:
            import NemoMaya
            return NemoMaya.get_version()
        except:
            return "<unknown>"

    def create_controllers(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(dayu_widgets.MDivider("Controllers"))

        self.list_glob = QtWidgets.QListWidget()
        self.list_glob.setFixedHeight(60)
        layout.addWidget(self.list_glob)

        layout_list = QtWidgets.QHBoxLayout()

        text_controller_patterns = dayu_widgets.MLineEdit("<GLOB>")
        label_head = dayu_widgets.MLabel(text="Pattern").mark().secondary()
        label_head.setAlignment(QtCore.Qt.AlignCenter)
        label_head.setFixedWidth(60)
        text_controller_patterns.set_prefix_widget(label_head)
        layout_list.addWidget(text_controller_patterns)

        btn_remove_current = dayu_widgets.MPushButton("Remove")
        btn_remove_current.clicked.connect(lambda: self.list_glob.takeItem(self.list_glob.currentRow()
                                                                           if self.list_glob.hasFocus() else self.list_prefix.count() - 1))
        layout_list.addWidget(btn_remove_current)
        btn_add_pattern = dayu_widgets.MPushButton("Add")
        btn_add_pattern.clicked.connect(lambda: self.list_glob.addItem(text_controller_patterns.text()))
        layout_list.addWidget(btn_add_pattern)
        layout.addLayout(layout_list)

        self.tags_controllers = dayu_widgets.MCheckBoxGroup()
        self.tags_controllers.set_button_list(["Curve", "Surface", "Free", "Visible"])
        layout.addWidget(self.tags_controllers)

        btn_controllers = dayu_widgets.MPushButton("Select Controllers")
        btn_controllers.clicked.connect(self.on_select_controllers)
        layout.addWidget(btn_controllers)

        layout_list = QtWidgets.QHBoxLayout()
        btn_append = dayu_widgets.MPushButton("Append")
        btn_append.clicked.connect(self.append_select_controllers)
        layout_list.addWidget(btn_append)
        btn_deslect = dayu_widgets.MPushButton("Deselect")
        btn_deslect.clicked.connect(self.deselect_controllers)
        layout_list.addWidget(btn_deslect)
        layout.addLayout(layout_list)

        return layout

    def get_controllers(self):
        patterns = [self.list_glob.item(row).text() for row in range(self.list_glob.count())]
        args = {'patterns': patterns}
        for x in self.tags_controllers.get_dayu_checked():
            args[str(x).lower()] = True

        from nemo.filter import scene_collect
        return scene_collect.get_controllers(**args)

    def is_valid_controller(self, obj):
        if cmds.nodeType(obj) not in {'transform', 'joint'}:
            QMessageBox.critical(self, '{} is not allowed for controller.'.format(obj),
                                 'Controller can only be transform or joint, not {}. Please make sure not selecting any shapes.'.format(cmds.nodeType(obj)))
            return False
        if cmds.nodeType(obj) == 'transform' and not cmds.listRelatives(obj, shapes=True):
            QMessageBox.critical(self, '{} is not allowed for controller.'.format(obj), 'Controller should have visible shapes, not empty transform.')
            return False
        return True

    def append_select_controllers(self):
        selection = cmds.ls(sl=True)
        if not all(self.is_valid_controller(x) for x in selection):
            return

        for x in selection:
            self.list_glob.addItem(x)
        self.on_select_controllers()

    def deselect_controllers(self):
        selection = cmds.ls(sl=True)
        if not all(self.is_valid_controller(x) for x in selection):
            return

        for x in selection:
            self.list_glob.addItem('!' + x)
        self.on_select_controllers()

    def on_select_controllers(self):
        cmds.select(self.get_controllers())
        cmds.warning('{} controllers are selected. use `ls -sl` to list them.'.format(len(cmds.ls(sl=True))))

    def create_shapes(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(dayu_widgets.MDivider("Shapes"))

        self.list_prefix = QtWidgets.QListWidget()
        self.list_prefix.setFixedHeight(60)
        layout.addWidget(self.list_prefix)

        layout_list = QtWidgets.QHBoxLayout()
        text_shape_groups = dayu_widgets.MLineEdit("<keyword>")
        label_head = dayu_widgets.MLabel(text="Group").mark().secondary()
        label_head.setAlignment(QtCore.Qt.AlignCenter)
        label_head.setFixedWidth(60)
        text_shape_groups.set_prefix_widget(label_head)
        layout_list.addWidget(text_shape_groups)

        btn_remove_current = dayu_widgets.MPushButton("Remove")
        btn_remove_current.clicked.connect(lambda: self.list_prefix.takeItem(self.list_prefix.currentRow()
                                                                             if self.list_prefix.hasFocus() else self.list_prefix.count() - 1))
        layout_list.addWidget(btn_remove_current)
        btn_add_pattern = dayu_widgets.MPushButton("Add")
        btn_add_pattern.clicked.connect(lambda: self.list_prefix.addItem(text_shape_groups.text()))
        layout_list.addWidget(btn_add_pattern)
        layout.addLayout(layout_list)

        btn_add_groups = dayu_widgets.MPushButton("Add Group")
        btn_add_groups.clicked.connect(self.on_add_groups)
        layout.addWidget(btn_add_groups)

        btn_shapes = dayu_widgets.MPushButton("Select Shapes")
        btn_shapes.clicked.connect(self.on_select_shapes)
        layout.addWidget(btn_shapes)
        return layout

    def on_add_groups(self):
        selection = cmds.ls(sl=True)
        for obj in selection:
            if cmds.nodeType(obj) != 'transform' or cmds.listRelatives(obj, shapes=True):
                QMessageBox.critical(self, '{} is invalid.'.format(obj), 'Only accept group.')
                return

        for x in selection:
            self.list_prefix.addItem(x + '|')
        self.on_select_controllers()

    def get_shapes(self):
        from nemo.filter import scene_collect
        patterns = [self.list_prefix.item(row).text() for row in range(self.list_prefix.count())]
        return scene_collect.get_meshes(patterns, self.get_controllers())

    def on_select_shapes(self):
        cmds.select(self.get_shapes())
        print('{} meshes are selected'.format(len(cmds.ls(sl=True))))

    def create_export(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(dayu_widgets.MDivider("Export"))

        self.text_name = dayu_widgets.MLineEdit("Dummy")
        label_head = dayu_widgets.MLabel(text="Name").mark().secondary()
        label_head.setAlignment(QtCore.Qt.AlignCenter)
        label_head.setFixedWidth(60)
        self.text_name.set_prefix_widget(label_head)
        layout.addWidget(self.text_name)

        layout_dir = QtWidgets.QHBoxLayout()
        self.browser_dir_export = dayu_widgets.MClickBrowserFolderToolButton()
        layout_dir.addWidget(self.browser_dir_export)
        label_dir = dayu_widgets.MLabel("<Select Output Folder>")
        label_dir.set_elide_mode(QtCore.Qt.ElideLeft)
        layout_dir.addWidget(label_dir)
        self.browser_dir_export.sig_folder_changed.connect(label_dir.setText)
        layout.addLayout(layout_dir)

        import glob
        addons = [os.path.splitext(os.path.basename(x))[0] for x in glob.glob("{}/*.json".format(os.environ['NEMO_MODULES']))]
        addons = [x for x in addons if x not in {"builtin", "matrixNodes"}]
        self.tags_addons = dayu_widgets.MCheckBoxGroup()
        self.tags_addons.set_button_list(addons)
        layout.addWidget(self.tags_addons)

        self.btn_export = dayu_widgets.MPushButton("Parse")
        self.btn_export.clicked.connect(self.on_export)
        layout.addWidget(self.btn_export)

        self.progress_parse = dayu_widgets.MProgressBar().auto_color()
        layout.addWidget(self.progress_parse)
        return layout

    def on_export(self):
        from nemo.m2n import m2n
        path = self.browser_dir_export.dayu_path
        if path is None:
            QMessageBox.critical(self, "Error", "Must Select Output Folder First")
            return

        name = self.text_name.text()
        if "Dummy" == name:
            if QMessageBox.StandardButton.No == QMessageBox.question(self, "Name", "Is Dummy the correct name?"):
                return
        try:
            cmds.optionVar(sv=('NEMO_EXPORT_CONFIG', self.save_config()))

            self.check()
            m2n.export(name,
                       self.get_controllers(),
                       self.get_shapes(),
                       str(path),
                       addons=self.tags_addons.get_dayu_checked(),
                       debug=True,
                       material=True,
                       callback=lambda percent: self.progress_parse.setValue(percent))
        except Exception as e:
            print("Nemo Export Error:", e)
            QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.information(self, "Success", '{} has been exported to {}'.format(name, path))

    def save_config(self):
        config = dict()
        config['ctrl_pattern'] = [self.list_glob.item(row).text() for row in range(self.list_glob.count())]
        config['ctrl_tags'] = [str(x) for x in self.tags_controllers.get_dayu_checked()]
        config['shapes_keyword'] = [self.list_prefix.item(row).text() for row in range(self.list_prefix.count())]
        config['export_dir'] = str(self.browser_dir_export.dayu_path)
        config['addons'] = [str(x) for x in self.tags_addons.get_dayu_checked()]
        return json.dumps(config)

    def load_config(self, config):
        try:
            for pattern in config.get('ctrl_pattern', ['*']):
                self.list_glob.addItem(pattern)
            self.tags_controllers.set_dayu_checked(config.get('ctrl_tags', ["Curve", "Free", "Visible"]))
            for keyword in config.get('shapes_keyword', []):
                self.list_prefix.addItem(keyword)
            if 'export_dir' in config:
                self.browser_dir_export.set_dayu_path(config['export_dir'])
                self.browser_dir_export.sig_folder_changed.emit(self.browser_dir_export.get_dayu_path())
            self.tags_addons.set_dayu_checked(config.get('addons', ["quatNodes"]))
        except Exception:
            pass


def show():
    widget = WidgetNemoExporter()
    from dayu_widgets import dayu_theme
    dayu_theme.apply(widget)
    widget.show()


if __name__ == "__main__":
    show()
