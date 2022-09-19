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

import json
import os
from . import import_controllers
from nemo import utils
from maya import cmds


def inv_var_name(text):
    return text.replace("__DOT__", '.')


def connect_matrix_to_transform(src, obj):
    node_decompose = cmds.createNode('decomposeMatrix')
    cmds.connectAttr(src, '%s.inputMatrix' % node_decompose)

    for attr in {'translate', 'rotate', 'scale'}:
        source = '{}.output{}'.format(node_decompose, attr.capitalize())
        dest = '{}.{}'.format(obj, attr)
        if cmds.getAttr(dest, lock=True):
            cmds.setAttr(dest, lock=False)
            cmds.connectAttr(source, dest)
            cmds.setAttr(dest, lock=True)
        else:
            cmds.connectAttr(source, dest)


def assemble(path_config, path_scene, path_bin, path_resource, path_shading, identifier, dll_mode, relative_path=True):
    with open(path_scene) as f:
        import_controllers.import_from(json.load(f))

    with open(path_config) as f:
        config = json.load(f)

    if dll_mode:
        config['bin'] = os.path.basename(path_bin) if relative_path else path_bin
        config['resource'] = os.path.basename(path_resource) if relative_path else path_resource
        with open(path_config, 'w') as f:
            json.dump(config, f)
        cmds.loadPlugin('Nemo', quiet=True)
    else:
        cmds.loadPlugin(path_bin)
    cmds.loadPlugin('matrixNodes', quiet=True)

    if dll_mode:
        root = utils.get_root()
        node = cmds.createNode('Nemo', name='NEMO__{}'.format(identifier), p=root)
    else:
        node = cmds.createNode(identifier)

    ## import rig
    for x in config["inputs"] + config["outputs"]:
        name = x["name"]
        typename = x["type"]
        obj, attr = inv_var_name(name).split('.')
        if dll_mode:
            if "Float" == typename:
                cmds.addAttr(node, ln=name, at="float")
            elif "Angle" == typename:
                cmds.addAttr(node, ln=name, at="doubleAngle")
            elif "Vec3" == typename:
                cmds.addAttr(node, ln=name, at="float3")
                cmds.addAttr(node, ln=name + 'X', at="float", parent=name)
                cmds.addAttr(node, ln=name + 'Y', at="float", parent=name)
                cmds.addAttr(node, ln=name + 'Z', at="float", parent=name)
            elif "Euler" == typename:
                cmds.addAttr(node, ln=name, at="double3")
                cmds.addAttr(node, ln=name + 'X', at="doubleAngle", parent=name)
                cmds.addAttr(node, ln=name + 'Y', at="doubleAngle", parent=name)
                cmds.addAttr(node, ln=name + 'Z', at="doubleAngle", parent=name)
            elif "Mat4" == typename:
                cmds.addAttr(node, ln=name, at="fltMatrix")
            elif "Bool" == typename:
                cmds.addAttr(node, ln=name, at="bool")
            elif "Int" == typename:
                cmds.addAttr(node, ln=name, at="long")
            elif "Mesh" == typename:
                cmds.addAttr(node, ln=name, dt="mesh")
            else:
                assert False, typename

        is_output = "affectings" in x
        if is_output:
            if attr == 'worldMesh0':
                dest = '{}.inMesh'.format(obj)
                if dll_mode:
                    slot = cmds.listRelatives(obj, p=True)[0]
                    cmds.connectAttr('{}.write'.format(node), '{}.visibility'.format(slot))
            elif attr == 'worldSpace0':
                dest = '{}.create'.format(obj)
            elif attr == 'parentMatrix0':
                dest = cmds.listRelatives(obj, p=True)[0]
            elif attr == 'lodVisibility':
                segments = cmds.ls(obj, long=True)[0].split('|')[1:]
                for x in segments[::-1]:
                    if x.startswith('NEMO_'):
                        dest = '{}.visibility'.format(x)
                        break
                else:
                    dest = '{}.visibility'.format(obj)
            else:
                dest = '{}.{}'.format(obj, attr)
            if typename == 'Mat4':
                connect_matrix_to_transform('{}.{}'.format(node, name), dest)
            else:
                if cmds.getAttr(dest, lock=True):
                    cmds.setAttr(dest, lock=False)
                    cmds.connectAttr('{}.{}'.format(node, name), dest)
                    cmds.setAttr(dest, lock=True)
                else:
                    cmds.connectAttr('{}.{}'.format(node, name), dest)
        else:
            cmds.connectAttr('{}.{}'.format(obj, attr), '{}.{}'.format(node, name))

    if dll_mode:
        cmds.setAttr('{}.write'.format(node), True)
        cmds.setAttr('{}.nemo'.format(node), os.path.basename(path_config) if relative_path else path_config, type="string")
        cmds.setAttr('{}.shading'.format(node), os.path.basename(path_shading) if relative_path else path_shading, type="string")
    else:
        cmds.setAttr('{}.resource'.format(node), path_resource, type="string")

    if path_shading:
        ## assign shaders based on MAT json
        with open(path_shading) as f:
            data = json.load(f)
        shading_data = dict()
        for shader, members in data.items():
            if shader == 'lambert1':
                sg = 'initialShadingGroup'
            else:
                sg = cmds.listConnections(shader, t='shadingEngine')
                if len(sg) != 1:
                    raise RuntimeError("Shader {} should have exactly one shading group.".format(shader))
                sg = sg[0]
            shading_data[sg] = members
        for sg, components in shading_data.items():
            cmds.sets(components, e=True, forceElement=sg)

    if dll_mode:
        cmds.setAttr('{}.write'.format(node), False)

        node_proxy = cmds.createNode("mesh", name='NEMO_PROXY__{}'.format(identifier), p=root)
        cmds.connectAttr('{}.proxy'.format(node), '{}.inMesh'.format(node_proxy))
        node_reverse = cmds.createNode('reverse')
        cmds.connectAttr('{}.write'.format(node), '{}.inputX'.format(node_reverse))
        cmds.connectAttr('{}.outputX'.format(node_reverse), '{}.visibility'.format(node_proxy))

        import maya.api.OpenMaya as om2
        num_materials = len(shading_data)
        points = om2.MPointArray()
        points.append(om2.MPoint(0, 0, 0))
        points.append(om2.MPoint(0, 0, 0))
        points.append(om2.MPoint(0, 0, 0))
        counts = om2.MIntArray()
        connections = om2.MIntArray()
        for _ in range(num_materials):
            counts.append(3)
            connections.append(0)
            connections.append(1)
            connections.append(2)
        mesh = om2.MFnMesh()
        mesh.create(points, counts, connections, parent=om2.MGlobal.getSelectionListByName(root).getDependNode(0))
        for i, (sg, _) in enumerate(shading_data.items()):
            cmds.sets("{}.f[{}]".format(mesh.name(), i), e=True, forceElement=sg)
        cmds.rename(mesh.name(), 'NEMO_MATERIALS__{}'.format(identifier))
