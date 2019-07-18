import unittest
import os

import pywavefront.texture
from utils import fixture


class TestTexture(unittest.TestCase):

    def testPathedImageName(self):
        """For Texture objects, the image name should be the last component of the path."""
        my_texture = pywavefront.texture.Texture(fixture('4x4.png'))
        self.assertEqual(my_texture.path, fixture('4x4.png'))

    def testMissingFile(self):
        """Referencing a missing texture file should raise an exception."""
        texture = pywavefront.texture.Texture('missing.file.do.not.create')
        self.assertFalse(texture.exists())

    def testPathVsName(self):
        texture = pywavefront.texture.Texture('somefile', 'path/to/somefile')
        self.assertEqual(texture.name, 'somefile')
        self.assertEqual(texture.path, 'path/to/somefile')
        self.assertEqual(texture.image_name, 'somefile')

        texture.name = "test1"
        self.assertEqual(texture.name, 'test1')
        self.assertEqual(texture.image_name, 'test1')

        texture.image_name = "test2"
        self.assertEqual(texture.name, 'test2')
        self.assertEqual(texture.image_name, 'test2')

        texture.path = "some/path"
        self.assertEqual(texture.path, 'some/path')
