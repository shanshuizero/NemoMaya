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

import itertools
from maya import cmds


def export(shapes, controllers, path_export):
    shading_groups = set()
    for shape in shapes:
        sg = cmds.listConnections(shape, type='shadingEngine')
        if not sg:
            raise RuntimeError("no shading group for shape {}".format(shape))
        shading_groups.update(sg)

    materials = [cmds.listConnections('{}.surfaceShader'.format(sg), s=True, d=False)[0] for sg in shading_groups]
    if not materials:
        return None

    objects = set(itertools.chain(*[cmds.listHistory(mat, pdo=True) for mat in materials]))
    cmds.select(objects, ne=True)
    cmds.select(shading_groups, ne=True, add=True)
    cmds.file(path_export, typ='mayaAscii', ess=True, f=True)

    mapping = dict()
    for sg in shading_groups:
        members = []
        for x in cmds.sets(sg, q=True):
            if '.' in x:
                geo, suffix = x.split('.')
                if cmds.nodeType(geo) != 'mesh':
                    for shape in cmds.listRelatives(geo, s=True, ni=True, typ='mesh'):
                        if shape not in shapes:
                            continue
                        members.append('{}.{}'.format(shape, suffix))
            else:
                if x not in shapes:
                    continue
                members.append(x)
        mat = cmds.listConnections('{}.surfaceShader'.format(sg), s=True, d=False)[0]
        mapping[mat] = members

    connections = []
    for obj in objects:
        drivers = set(cmds.listConnections(obj, s=True, d=False) or [])
        for ctrl in controllers:
            if ctrl in drivers:
                edges = cmds.listConnections(obj, c=True, p=True, s=True, d=False)
                for i in range(len(edges))[::2]:
                    src = edges[i + 1]
                    dest = edges[i]
                    if src.split('.')[0] == ctrl:
                        connections.append((src, dest))

    return mapping, connections
