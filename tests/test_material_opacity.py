import gzip

import pytest

import pywavefront
from pywavefront.material import MaterialParser


COLORS = [('Ka', 'ambient'), ('Kd', 'diffuse'),
          ('Ks', 'specular'), ('Ke', 'emissive')]


@pytest.mark.parametrize('statement,attribute', COLORS)
@pytest.mark.parametrize(
    'opacity,expected', [('d 0.25', 0.25), ('Tr 0.75', 0.25), ('d 0', 0.0), ('Tr 0', 1.0)])
@pytest.mark.parametrize('before', [False, True])
def test_color_preserves_opacity(tmp_path, statement, attribute, opacity, expected, before):
    color = statement + ' 0.2 0.3 0.4'
    lines = [opacity, color] if before else [color, opacity]
    path = tmp_path / 'material.mtl'
    path.write_text('newmtl paint\n' + '\n'.join(lines) + '\n')
    material = MaterialParser(str(path), strict=True).materials['paint']
    assert material.transparency == expected
    assert getattr(material, attribute) == [0.2, 0.3, 0.4, expected]


@pytest.mark.parametrize('statement,attribute', COLORS)
def test_default_opaque_color(tmp_path, statement, attribute):
    path = tmp_path / 'material.mtl'
    path.write_text('newmtl paint\n' + statement + ' 0.2 0.3 0.4\n')
    material = MaterialParser(str(path), strict=True).materials['paint']
    assert getattr(material, attribute) == [0.2, 0.3, 0.4, 1.0]


@pytest.mark.parametrize('statement,attribute', COLORS)
def test_abbreviated_color_preserves_opacity(tmp_path, statement, attribute):
    path = tmp_path / 'material.mtl'
    path.write_text('newmtl paint\nd 0.25\n' + statement + ' 0.2\n')
    material = MaterialParser(str(path), strict=True).materials['paint']
    assert getattr(material, attribute)[3] == 0.25


@pytest.mark.parametrize('statement,attribute', COLORS)
def test_explicit_alpha_keeps_existing_behavior(tmp_path, statement, attribute):
    path = tmp_path / 'material.mtl'
    path.write_text('newmtl paint\nd 0.25\n' + statement + ' 0.2 0.3 0.4 0.8\n')
    material = MaterialParser(str(path), strict=True).materials['paint']
    assert getattr(material, attribute) == [0.2, 0.3, 0.4, 0.8]


@pytest.mark.parametrize('compressed', [False, True])
def test_opacity_is_per_material_in_loaded_scene(tmp_path, compressed):
    colors = ''.join(statement + ' 0.2 0.3 0.4\n' for statement, _ in COLORS)
    mtl = 'newmtl glass\nd 0.25\n' + colors + 'newmtl solid\n' + colors
    mtl_path = tmp_path / ('material.mtl.gz' if compressed else 'material.mtl')
    opener = gzip.open if compressed else open
    with opener(str(mtl_path), 'wb') as stream:
        stream.write(mtl.encode('ascii'))
    obj_path = tmp_path / 'triangle.obj'
    obj_path.write_text('mtllib ' + mtl_path.name + '\nv 0 0 0\nv 1 0 0\nv 0 1 0\n'
                        'usemtl glass\nf 1 2 3\nusemtl solid\nf 1 2 3\n')
    scene = pywavefront.Wavefront(str(obj_path), strict=True)
    for name, alpha in [('glass', 0.25), ('solid', 1.0)]:
        material = scene.materials[name]
        assert material.transparency == alpha
        assert len(material.vertices) == 9
        for _, attribute in COLORS:
            assert getattr(material, attribute) == [0.2, 0.3, 0.4, alpha]
