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
