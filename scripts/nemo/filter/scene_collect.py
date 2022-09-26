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
from maya import cmds
from nemo import utils
import maya.api.OpenMaya as om2


def get_enum_field(plug):
    from maya import cmds
    result = []
    cursor = -1
    for name_value in cmds.addAttr(plug, q=True, enumName=True).split(':'):
        if '=' in name_value:
            name, value = name_value.rsplit('=', 1)
        else:
            name, value = name_value, cursor + 1
        result.append((name, int(value)))
        cursor = int(value)
    return result


def list_channel_box(obj):
    _attributes = (cmds.listAttr(obj, k=True) or []) + \
        (cmds.listAttr(obj, cb=True) or [])
    attributes = []
    for attr in _attributes:
        plug = '{}.{}'.format(obj, attr)
        if cmds.getAttr(plug, lock=True):
            continue
        attr_type = cmds.getAttr(plug, type=True)
        if attr_type in {'string', 'double3'}:
            continue
        if attr_type == 'enum' and attr != 'rotateOrder' and len(get_enum_field(plug)) == 1:
            continue
        attributes.append(attr)
    return attributes


def leaves_of_plug(plug):
    if plug.isArray:
        return sum([leaves_of_plug(plug.elementByLogicalIndex(i)) for i in plug.getExistingArrayAttributeIndices()], [])
    elif plug.isCompound:
        return sum([leaves_of_plug(plug.child(i)) for i in range(plug.numChildren())], [plug])
    else:
        return [plug]


def get_history(plug):
    sources = cmds.listConnections(plug, p=True, s=True, d=False)
    if not sources:
        sources = []
        maya_plug = om2.MGlobal.getSelectionListByName(plug).getPlug(0)
        node = om2.MFnDependencyNode(maya_plug.node())
        for attr in node.getAffectingAttributes(maya_plug.attribute()):
            plug = node.findPlug(attr, True)
            if '-1' in plug.name():
                continue
            sources.extend(x.name() for x in leaves_of_plug(plug))

    if not sources:
        return [plug]

    return sum([get_history(x) for x in set(sources)], [])


def is_visibility_always_off(obj, controllers):
    if cmds.getAttr('{}.visibility'.format(obj)):
        return False
    plug = '{}.visibility'.format(obj)
    history = get_history(plug)
    if not history:
        return True
    for x in history:
        if x == plug:
            continue
        node = x[:x.find('.')]
        if node not in controllers:
            continue
        if cmds.getAttr(x, lock=True):
            continue
        if cmds.getAttr(x, cb=True) or cmds.getAttr(x, k=True):
            return False
    return True


def is_world_visibility_always_off(obj, controllers):
    shapes = cmds.listRelatives(obj, shapes=True, ni=True)
    if shapes and all(is_visibility_always_off(x, controllers) for x in shapes):
        return True

    segments = cmds.ls(obj, long=True)[0].split('|')[1:]
    transforms = ['|'.join(segments[:i]) for i in range(1, 1 + len(segments))]
    for x in transforms:
        if is_visibility_always_off(x, controllers):
            return True
    return False


def is_channel_box_locked(ctrl):
    for x in list_channel_box(ctrl):
        if not cmds.getAttr("{}.{}".format(ctrl, x), lock=True) and x != "visibility":
            return False
    return True


def is_channel_box_driven(ctrl):
    default_attributes = [
        'translate', 'translateX', 'translateY', 'translateZ', 'rotate', 'rotateX', 'rotateY', 'rotateZ', 'scale', 'scaleX', 'scaleY', 'scaleZ'
    ]
    for x in list_channel_box(ctrl) + default_attributes:
        if cmds.listConnections("{}.{}".format(ctrl, x), s=True, d=False):
            return True
    return False


def get_extra(ctrl):
    parent = cmds.listRelatives(ctrl, p=True)
    if not parent:
        return None
    parent = parent[0]
    if not cmds.listRelatives(parent, p=True):
        return None
    if cmds.listRelatives(parent, shapes=True) or not utils.is_matrix_identity(cmds.xform(parent, q=True, m=True, os=True)):
        return None
    return None if is_channel_box_driven(parent) else parent


def match(pattern, curve, surface, free, visible):
    objects = cmds.ls(pattern, transforms=True)
    controllers = []
    for obj in objects:
        shapes = cmds.listRelatives(obj, shapes=True, ni=True, pa=True) or []
        pass_test = False
        for s in shapes:
            if cmds.getAttr('{}.overrideEnabled'.format(s)) and cmds.getAttr('{}.overrideDisplayType'.format(s)):
                continue
            if curve and cmds.nodeType(s) == 'nurbsCurve':
                pass_test = True
            if surface and cmds.nodeType(s) == "nurbsSurface":
                pass_test = True
            if not curve and not surface:
                pass_test = True
        if pass_test:
            controllers.append(obj)

    if free:
        controllers = [ctrl for ctrl in controllers if not is_channel_box_locked(ctrl)]
    if visible:
        controllers = [ctrl for ctrl in controllers if not is_world_visibility_always_off(ctrl, controllers)]
    return controllers


def get_controllers(patterns, curve=True, surface=False, free=True, visible=True):
    results = []

    for pattern in patterns:
        if pattern.startswith('!'):
            continue
        results.extend(match(pattern, curve, surface, free, visible))

    # negative select should happen at the end
    for pattern in patterns:
        if not pattern.startswith('!'):
            continue
        to_erase = match(pattern[1:], curve, surface, free, visible)
        results = [x for x in results if x not in to_erase]

    return results


def get_meshes(patterns, controllers):
    shapes = []
    for shape in cmds.ls(type='mesh', long=True, ni=True):
        if any(x in shape for x in patterns) and not is_world_visibility_always_off(shape, controllers):
            shapes.append(shape)
    return shapes