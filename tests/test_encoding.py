import codecs
import gzip

import pytest

import pywavefront


def write_source(path, text, compressed, bom=False, encoding='utf-8'):
    data = text.encode(encoding)
    if bom:
        data = codecs.BOM_UTF8 + data
    opener = gzip.open if compressed else open
    with opener(str(path), 'wb') as stream:
        stream.write(data)


@pytest.mark.parametrize(
    'obj_bom,mtl_bom', [(False, False), (True, False), (False, True), (True, True)])
@pytest.mark.parametrize('compressed', [False, True])
@pytest.mark.parametrize('encoding', [None, 'UTF8', 'utf-8-sig'])
@pytest.mark.parametrize('strict', [False, True])
def test_utf8_bom(tmp_path, obj_bom, mtl_bom, compressed, encoding, strict):
    suffix = '.gz' if compressed else ''
    obj_path = tmp_path / ('triangle.obj' + suffix)
    mtl_path = tmp_path / ('triangle.mtl' + suffix)
    # U+FEFF inside a material name is data, not a file signature.
    name = 'caf\u00e9\ufeffpaint'
    obj = ('v 0 0 0\nv 1 0 0\nv 0 1 0\nmtllib {0}\n'
           'usemtl {1}\nf 1 2 3\n').format(mtl_path.name, name)
    mtl = 'newmtl {0}\nKd 0.25 0.5 0.75\n'.format(name)
    write_source(obj_path, obj, compressed, obj_bom)
    write_source(mtl_path, mtl, compressed, mtl_bom)
    kwargs = {'strict': strict, 'collect_faces': True}
    if encoding is not None:
        kwargs['encoding'] = encoding
    scene = pywavefront.Wavefront(str(obj_path), **kwargs)
    assert scene.vertices == [(0., 0., 0.), (1., 0., 0.), (0., 1., 0.)]
    assert scene.mesh_list[0].faces == [[0, 1, 2]]
    material = scene.materials[name]
    assert scene.mesh_list[0].materials == [material]
    assert material.diffuse[:3] == [0.25, 0.5, 0.75]
    assert material.vertices == [0., 0., 0., 1., 0., 0., 0., 1., 0.]


@pytest.mark.parametrize('encoding', ['utf-16', 'iso-8859-1'])
@pytest.mark.parametrize('compressed', [False, True])
def test_other_encodings(tmp_path, encoding, compressed):
    suffix = '.gz' if compressed else ''
    path = tmp_path / ('triangle.obj' + suffix)
    obj = 'v 0 0 0\nv 1 0 0\nv 0 1 0\no caf\u00e9\nf 1 2 3\n'
    write_source(path, obj, compressed, encoding=encoding)
    scene = pywavefront.Wavefront(str(path), strict=True, encoding=encoding,
                                  collect_faces=True)
    assert scene.meshes['caf\u00e9'].faces == [[0, 1, 2]]
    assert len(scene.vertices) == 3
