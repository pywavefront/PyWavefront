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
