import os
import unittest
import mock
from io import BytesIO
import json
from datetime import datetime
from pywavefront import ObjParser, Wavefront
from pywavefront.parser import Parser
from pywavefront.exceptions import PywavefrontException
from pywavefront.cache import cache_name, meta_name


@mock.patch('pywavefront.parser.Parser.auto_post_parse', new=False)
class CacheTest(unittest.TestCase):
    """Create and load cache for a specific obj file"""
    maxDiff = None
    obj_file = 'simple.obj'

    def load_obj(self, filename, fake_io=None):
        """Helper method loading files with proper mocks"""
        if not fake_io:
            self.fake_io = FakeIO()

        if not fake_io:
            scene = Wavefront(prepend_dir(filename), cache=True)

        with mock.patch("pywavefront.cache.gzip.open", new=self.fake_io):
            with mock.patch("pywavefront.cache.open", new=self.fake_io):
                with mock.patch("pywavefront.cache.os.path.exists", new=self.fake_io.exisis):
                    if fake_io:
                        scene = Wavefront(prepend_dir(filename), cache=True)
                    scene.parser.post_parse()

        self.meta_file = self.obj_file + '.json'
        self.cache_file = self.obj_file + '.bin'
        return scene

    @property
    def meta(self):
        return self.fake_io[self.meta_file].json()

    @property
    def cache(self):
        return self.fake_io[self.cache_file]

    def test_create(self):
        scene = self.load_obj(self.obj_file)

        # Sanity check cache data
        self.assertTrue(self.meta.get('version'), msg="Missing version info in meta file: {}".format(self.meta))
        self.assertEqual(self.meta['mtllibs'], scene.mtllibs)
        self.assertEqual(self.cache.size, sum(len(m.vertices) for m in scene.materials.values()) * 4)

    def test_load(self):
        # Load the file creating a cache
        scene_pre = self.load_obj(self.obj_file)
        # Load again using cache
        scene_post = self.load_obj(self.obj_file, self.fake_io)

        self.assertFalse(scene_pre.parser.cache_loaded, msg="File was loaded from cache")
        self.assertTrue(scene_post.parser.cache_loaded, msg="File was not loaded from cache")

        # Compare pre and post cache
        self.assertEqual(sorted(scene_pre.materials.keys()), sorted(scene_post.materials.keys()))
        for name, pre_mat in scene_pre.materials.items():
            post_mat = scene_post.materials[name]
            self.assertNotEqual(pre_mat, post_mat)  # Ensure they are differnt objects!
            self.assertEqual(len(pre_mat.vertices), len(post_mat.vertices))
            for a, b in zip(pre_mat.vertices, post_mat.vertices):
                self.assertAlmostEqual(a, b, msg="{} != {}".format(pre_mat.vertices, post_mat.vertices))
            self.assertEqual(pre_mat.vertex_format, post_mat.vertex_format)
            self.assertEqual(pre_mat.name, post_mat.name)

    def test_missing_meta(self):
        # Load the file creating a cache
        scene_pre = self.load_obj(self.obj_file)

        # Be naughty deleting the meta file
        del self.fake_io[self.meta_file]

        # Load again using cache
        scene_post = self.load_obj(self.obj_file, self.fake_io)
        # No cache loader should be created
        self.assertFalse(scene_pre.parser.cache_loaded)
        self.assertFalse(scene_post.parser.cache_loaded)


@mock.patch('pywavefront.parser.Parser.auto_post_parse', new=False)
class CacheTestNoMaterials(CacheTest):
    obj_file = 'simple_no_mtl.obj'


class FakeFileExists(object):

    def __init__(self, fake_io):
        self.fake_io = fake_io

    def __call__(self, value):
        return self.fake_io.exists(value)


class FakeIO(object):
    """A collection of files written during a mock session"""

    def __init__(self):
        self.files = {}
        self.exisis = FakeFileExists(self)

    def __call__(self, name, mode, *args, **kwargs):
        """Simulates open()"""
        fake_file = self.files.get(name)

        if not fake_file:
            if 'w' in mode:
                fake_file = FakeFile(name, mode)
                self.files[name] = fake_file
            else:
                raise IOError("File not found: {}\n{}".format(name, self.files))

        return fake_file

    def exists(self, value):
        return self.files.get(value) is not None

    def __getitem__(self, name):
        return self.files[prepend_dir(name)]

    def __delitem__(self, name):
        del self.files[prepend_dir(name)]

class FakeFile(object):
    """Fake file object"""

    def __init__(self, name, mode):
        self.mode = mode
        self.name = name
        self.data = BytesIO()
        self.size = 0

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def read(self, length=-1):
        if length == -1:
            return self.data.read()

        return self.data.read(length)

    def write(self, data):
        if not 'b' in self.mode:
            data = data.encode()

        self.data.write(data)

    def close(self):
        self.size = self.data.tell()
        self.data.seek(0)

    def contents(self):
        cont = self.data.read()
        self.data.seek(0)
        return cont

    def json(self):
        d = self.contents().decode()
        return json.loads(d)


def prepend_dir(file):
    return os.path.join(os.path.dirname(__file__), file)
