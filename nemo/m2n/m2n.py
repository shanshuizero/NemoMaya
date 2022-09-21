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

import os
import json
import shutil
import imp
import tempfile
import zipfile

from maya import cmds

from exporter import Exporter
from get_io import get_io
import export_controllers
import export_materials


def export(identifier, controllers, shapes, project_dir, addons=[], debug=False, callback=None, material=False):
    inputs, outputs = get_io(controllers, shapes)

    tmpdirname = tempfile.mkdtemp()
    scene_data = export_controllers.export(identifier, controllers, shapes)
    if material:
        material_mapping, material_drivers = export_materials.export([cmds.ls(x)[0] for x in shapes], controllers,
                                                                     '{}/{}__MAT.ma'.format(tmpdirname, identifier))
        path_shading = '{}/{}__MAT.json'.format(tmpdirname, identifier)
        with open(path_shading, 'w') as f:
            json.dump(material_mapping, f)
        scene_data['connections'] = material_drivers

    path_scene = '{}/{}__SCENE.json'.format(tmpdirname, identifier)
    with open(path_scene, 'w') as f:
        json.dump(scene_data, f)

    import NemoMaya
    exporter = Exporter(NemoMaya.Parser, debug)
    exporter.set_project_dir(tmpdirname)
    exporter.set_identifier(identifier)

    exporter.set_modules_dir(os.environ['NEMO_MODULES'])
    for plugin in ['matrixNodes'] + addons:
        cmds.loadPlugin(plugin, quiet=True)
        exporter.append_module(plugin)

    exporter.init()

    addons_data = []
    for x in addons:
        spec_path = '{}/{}.py'.format(os.environ['NEMO_MODULES'], x)
        if not os.path.exists(spec_path):
            continue
        mod = imp.load_source(x, spec_path)
        addons_data += mod.add_custom_parameters(exporter.parser)

    if not exporter.parse(inputs, outputs, callback):
        for x in os.listdir(tmpdirname):
            if os.path.splitext(x)[-1] == '.txt':
                shutil.move('{}/{}'.format(tmpdirname, x), '{}/{}'.format(project_dir, x))
        raise RuntimeError("parsing maya file failed, maybe some features unspported yet, please check log at '{}' for details.".format(project_dir))
    # WARNING: addons_data can only be dropped after this moment as parsing done.
    del addons_data

    path_graph = '{}/{}__GRAPH.json'.format(project_dir, identifier)
    path_export = '{}/{}__EXPORT.zip'.format(project_dir, identifier)
    for x in [path_graph, path_export]:
        if os.path.exists(x):
            raise RuntimeError("{} already exist".format(x))
    shutil.move(exporter.path_graph(), path_graph)

    with zipfile.ZipFile(path_export, 'w') as zip:
        for x in os.listdir(tmpdirname):
            zip.write('{}/{}'.format(tmpdirname, x), x)

    shutil.rmtree(tmpdirname)
