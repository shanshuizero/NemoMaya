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

from maya import cmds

menupath = None


def on_load():
    import os
    if os.environ.get('NEMO_LOAD_TOPMENU', 'True').lower() in {'false', '0', 'f'}:
        return

    global menupath
    menupath = cmds.menu('nemo', label='Nemo', parent='MayaWindow')
    cmds.menuItem(label='Export', command='import nemo.interface.exporter as exporter; exporter.show()', parent=menupath)
    cmds.menuItem(label='Assemble', command='import nemo.interface.assembler as assembler; assembler.show()', parent=menupath)
    cmds.menuItem(label='Switch Preview', command='from nemo import shelf; shelf.on_switch("write")', parent=menupath)
    cmds.menuItem(label='Switch Cache', command='from nemo import shelf; shelf.on_switch("cache")', parent=menupath)


def on_unload():
    global menupath
    if menupath is None:
        return
    cmds.deleteUI(menupath, menu=True)
    menupath = None


def on_switch(attr):
    selection = cmds.ls(sl=True)
    nemo = cmds.ls(selection, type='Nemo')
    for x in selection:
        for shape in cmds.listRelatives(x, s=True):
            if cmds.nodeType(shape) == 'Nemo':
                nemo.append(shape)
    if not nemo:
        cmds.error("Must select nemo first")
        return
    for x in nemo:
        cmds.setAttr('{}.{}'.format(x, attr), not cmds.getAttr('{}.{}'.format(x, attr)))
        cmds.dgdirty(x)
