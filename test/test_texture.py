import unittest
import os

import pywavefront.texture

class TestTexture(unittest.TestCase):
    def setUp(self):
        self.folder = os.path.dirname(__file__) + '/'

    def testPathedImageName(self):
        "For Texture objects, the image name should be the last component of the path."
        my_texture = pywavefront.texture.Texture(self.folder + '4x4.png')
        self.assertEqual(my_texture.image_name, self.folder + '4x4.png')

    def testNonPowerOfTwoImage(self):
        "Texture images that have a non-power-of-two dimension should raise an exception."
        self.assertRaises(Exception, pywavefront.texture.Texture, self.folder + '3x4.png')

    def testMissingFile(self):
        "Referencing a missing texture file should raise an exception."
        self.assertRaises(Exception, pywavefront.texture.Texture, 'missing.file.do.not.create')
