import unittest
import os
from pathlib import Path

import pytest

import pywavefront
import pywavefront.texture
import utils


class TestTexture(unittest.TestCase):
    search_path = os.path

    def testPathedImageName(self):
        """For Texture objects, the image name should be the last component of the path."""
        texture = pywavefront.texture.Texture('4x4.png', search_path=utils.FIXTURE_PATH)
        self.assertEqual(texture.path, str(utils.fixture('4x4.png')))
        self.assertEqual(texture.name, '4x4.png')
        self.assertTrue(texture)
        self.assertEqual(texture.image_name, '4x4.png')
        self.assertEqual(texture.file_name, '4x4.png')
        self.assertTrue(os.path.exists(texture.find()))

    def testMissingFile(self):
        """Referencing a missing texture file should raise an exception."""
        texture = pywavefront.texture.Texture('missing.file.do.not.create', search_path='')
        self.assertFalse(texture.exists())
        with self.assertRaises(FileNotFoundError):
            texture.find()

    def testPathVsName(self):
        texture = pywavefront.texture.Texture('somefile', search_path=Path('path/to'))
        self.assertEqual(texture.name, 'somefile')
        self.assertEqual(texture.path, str(Path('path/to/somefile')))
        self.assertEqual(texture.image_name, 'somefile')

        texture.name = "test1"
        self.assertEqual(texture.name, 'test1')
        self.assertEqual(texture.image_name, 'test1')

        texture.image_name = "test2"
        self.assertEqual(texture.name, 'test2')
        self.assertEqual(texture.image_name, 'test2')

        texture.path = "some/path"
        self.assertEqual(texture.path, str(Path('some/path')))

    def test_options(self):
        params = [
            '-blendu on',
            '-blendv on',
            '-bm 1.0',
            '-boost 0.0',
            '-cc off',
            '-clamp off',
            '-imfchan l',
            '-mm 0.0 1.0',
            '-o 0.0 0.0 0.0',
            '-s 1.0 1.0 1.0',
            '-t 0.0 0.0 0.0',
            '-texres 1024',
            'path/to/sometexture.png',
        ]
        texture = pywavefront.texture.Texture(' '.join(params) , '')
        opts = texture.options
        self.assertEqual(opts.name, 'path/to/sometexture.png')
        self.assertEqual(opts.blendu, 'on')
        self.assertEqual(opts.blendv, 'on')
        self.assertEqual(opts.bm, 1.0)
        self.assertEqual(opts.boost, 0.0)
        self.assertEqual(opts.cc, 'off')
        self.assertEqual(opts.clamp, 'off')
        self.assertEqual(opts.imfchan, 'l')
        self.assertEqual(opts.mm, (0.0, 1.0))
        self.assertEqual(opts.o, (0.0, 0.0, 0.0))
        self.assertEqual(opts.s, (1.0, 1.0, 1.0))
        self.assertEqual(opts.t, (0.0, 0.0, 0.0))
        self.assertEqual(opts.texres, '1024')


@pytest.mark.parametrize('option,default', [('o', 0.0), ('s', 1.0), ('t', 0.0)])
@pytest.mark.parametrize('values', ['-2.5', '-2.5 3e-2', '-2.5 3e-2 4'])
@pytest.mark.parametrize('following', ['', ' -clamp on'])
def test_optional_vector_components(option, default, values, following):
    name = 'textures/2 diffuse.png'
    texture = pywavefront.texture.Texture(
        '-{} {}{} {}'.format(option, values, following, name), '')
    provided = tuple(float(value) for value in values.split())
    expected = provided + (default,) * (3 - len(provided))
    assert getattr(texture.options, option) == expected
    assert texture.name == name
    assert texture.options.clamp == ('on' if following else 'off')


@pytest.mark.parametrize('option', ['o', 's', 't'])
def test_vector_requires_numeric_first_component(option):
    with pytest.raises(ValueError):
        pywavefront.texture.Texture('-{} invalid texture.png'.format(option), '')


def test_repeated_vector_restores_defaults():
    texture = pywavefront.texture.Texture(
        '-s 2 3 4 -o 1 2 3 -s 5 -o 6 -t 7 8 texture.png', '')
    assert texture.options.s == (5.0, 1.0, 1.0)
    assert texture.options.o == (6.0, 0.0, 0.0)
    assert texture.options.t == (7.0, 8.0, 0.0)
    assert texture.name == 'texture.png'


def test_load_material_with_optional_vector_components(tmp_path):
    (tmp_path / 'model.mtl').write_text(
        'newmtl surface\n'
        'map_Kd -s 2 -clamp on diffuse.png\n'
        'map_Ka -o -0.5 0.25 ambient.png\n'
        'bump -t 0.1 -bm 0.5 bump.png\n')
    model = tmp_path / 'model.obj'
    model.write_text(
        'mtllib model.mtl\n'
        'v 0 0 0\nv 1 0 0\nv 0 1 0\n'
        'usemtl surface\nf 1 2 3\n')
    scene = pywavefront.Wavefront(model, collect_faces=True)
    material = scene.materials['surface']

    assert scene.mesh_list[0].faces == [[0, 1, 2]]
    assert material.vertices == [0, 0, 0, 1, 0, 0, 0, 1, 0]
    assert material.texture.name == 'diffuse.png'
    assert material.texture.options.s == (2.0, 1.0, 1.0)
    assert material.texture.options.clamp == 'on'
    assert material.texture_ambient.name == 'ambient.png'
    assert material.texture_ambient.options.o == (-0.5, 0.25, 0.0)
    assert material.texture_bump.name == 'bump.png'
    assert material.texture_bump.options.t == (0.1, 0.0, 0.0)
    assert material.texture_bump.options.bm == 0.5
