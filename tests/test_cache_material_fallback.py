import tempfile
import unittest
from pathlib import Path

from pywavefront import Wavefront


class CacheMaterialFallbackTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.obj = self.root / 'scene.obj'
        self.libraries = [self.root / 'red.mtl', self.root / 'green.mtl']
        for path, name, color in [
            (self.libraries[0], 'red', '1 0 0'),
            (self.libraries[1], 'green', '0 1 0'),
        ]:
            with path.open('w') as output:
                output.write('newmtl {}\nKd {}\n'.format(name, color))
        with self.obj.open('w') as output:
            output.write(
                'mtllib red.mtl\nmtllib green.mtl\n'
                'v 0 0 0\nv 1 0 0\nv 0 1 0\n'
                'usemtl red\nf 1 2 3\nusemtl green\nf 3 2 1\n'
            )
        self.original = Wavefront(str(self.obj), cache=True)
        self.assertFalse(self.original.parser.cache_loaded)

    def assert_cached_geometry(self, scene):
        self.assertTrue(scene.parser.cache_loaded)
        self.assertEqual(set(scene.materials), {'red', 'green'})
        for name, original in self.original.materials.items():
            loaded = scene.materials[name]
            self.assertEqual(list(loaded.vertices), original.vertices)
            self.assertEqual(loaded.vertex_format, original.vertex_format)

    def test_missing_libraries_with_material_creation(self):
        for missing in ((0,), (1,), (0, 1)):
            with self.subTest(missing=missing):
                contents = {}
                for i in missing:
                    with self.libraries[i].open() as source:
                        contents[i] = source.read()
                try:
                    for i in missing:
                        self.libraries[i].unlink()
                    # The OBJ loader already tolerates these missing files.
                    plain = Wavefront(str(self.obj), create_materials=True)
                    scene = Wavefront(str(self.obj), cache=True, create_materials=True)
                    self.assert_cached_geometry(scene)
                    for i, name in enumerate(('red', 'green')):
                        self.assertEqual(scene.materials[name].is_default, i in missing)
                        self.assertEqual(scene.materials[name].diffuse, plain.materials[name].diffuse)
                finally:
                    for i, text in contents.items():
                        with self.libraries[i].open('w') as output:
                            output.write(text)

    def test_missing_library_without_material_creation_remains_error(self):
        self.libraries[0].unlink()
        with self.assertRaises(IOError):
            Wavefront(str(self.obj), cache=True)

    def test_present_libraries_keep_their_materials(self):
        for create_materials in (False, True):
            with self.subTest(create_materials=create_materials):
                scene = Wavefront(str(self.obj), cache=True, create_materials=create_materials)
                self.assert_cached_geometry(scene)
                for name, original in self.original.materials.items():
                    self.assertEqual(scene.materials[name].diffuse, original.diffuse)
                    self.assertFalse(scene.materials[name].is_default)
