import unittest
import os
from pathlib import Path

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
