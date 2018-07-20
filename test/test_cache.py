from __future__ import unicode_literals

import os
import unittest
import mock
from io import BytesIO
import json
from datetime import datetime
from pywavefront import ObjParser, Wavefront
from pywavefront.parser import Parser
from pywavefront.exceptions import PywavefrontException

# Do not call post parse
Parser.auto_post_parse = False

def prepend_dir(file):
    return os.path.join(os.path.dirname(__file__), file)


class CacheTest(unittest.TestCase):
    maxDiff = None

    def test_create(self):
        """Test creating cache files"""
        obj_file = 'simple.obj'
        fake_io = FakeIO()
        scene = Wavefront(prepend_dir(obj_file), cache=True)

        with mock.patch("gzip.open", new=fake_io):
            with mock.patch("pywavefront.cache.open", new=fake_io):
                scene.parser.post_parse()

        # Inspect metadata
        meta = fake_io[prepend_dir(obj_file) + '.json'].json()
        data = {
            'version': '0.1',
            'materials': ['/Users/einarforselv/Documents/projects/contraz/PyWavefront/test/simple.mtl'],
            'vertex_buffers': [
                {'material': 'Material.simple', 'vertex_format': 'T2F_N3F_V3F', 'byte_offset': 0, 'byte_length': 96},
                {'material': 'Material2.simple', 'vertex_format': 'T2F_N3F_V3F', 'byte_offset': 96, 'byte_length': 96}
            ]
        }
        now = datetime.now()
        meta['created_at'] = now
        data['created_at'] = now
        # assert self.equal_dicts(meta, data)
        self.assertDictEqual(meta, data)

        # Inspect binary file
        data = fake_io[prepend_dir(obj_file) + '.bin'].contents()
        data_cmp = b'\x00\x00`A\x00\x00pA\x00\x00\xa0A\x00\x00\xa8A\x00\x00\xb0A\n\xd7#=\xcd\xccL=\x8f\xc2u=\x00\x00@A\x00\x00PA\x00\x00\xa0A\x00\x00\xa8A\x00\x00\xb0A\n\xd7#<\n\xd7\xa3<\x8f\xc2\xf5<\x00\x00 A\x00\x000A\x00\x00\xa0A\x00\x00\xa8A\x00\x00\xb0A)\\\x8f=\n\xd7\xa3=\xecQ\xb8=\x00\x00\x80?\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80?\x00\x00\x00\x80\x00\x00\x80\xbf\x00\x00\x00\x00\x00\x00\x80?\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80?\x00\x00\x00\x80\x00\x00\x80?\x00\x00\x00\x00\x00\x00\x80?\x00\x00\x00\x00\x00\x00\x80?\x00\x00\x00\x00\x00\x00\x80?\x00\x00\x00\x80\x00\x00\x80?\x00\x00\x00\x00\x00\x00\x80\xbf'
        self.assertEqual(data, data_cmp)


class FakeIO(object):

    def __init__(self):
        self.files = {}

    def __call__(self, name, mode, *args, **kwargs):
        """Simulates open()"""
        fake_file = self.files.get(name)

        if not fake_file:
            fake_file = FakeFile(name, mode)
            self.files[name] = fake_file

        return fake_file

    def __getitem__(self, name):
        return self.files[name]

class FakeFile(object):

    def __init__(self, name, mode):
        self.mode = mode
        self.name = name
        self.data = BytesIO()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def read(self):
        pass

    def write(self, data):
        if not 'b' in self.mode:
            data = data.encode()

        self.data.write(data)

    def close(self):
        self.data.seek(0)

    def contents(self):
        cont = self.data.read()
        self.data.seek(0)
        return cont

    def json(self):
        d = self.contents().decode()
        return json.loads(d)
