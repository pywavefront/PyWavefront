import unittest
import os

import pywavefront.texture
import pywavefront.visualization # power of two test

def prepend_dir(file):
    return os.path.join(os.path.dirname(__file__), file)

class TestTexture(unittest.TestCase):

    def testPathedImageName(self):
        "For Texture objects, the image name should be the last component of the path."
        my_texture = pywavefront.texture.Texture(prepend_dir('4x4.png'))
        self.assertEqual(my_texture.image_name, prepend_dir('4x4.png'))

    def testNonPowerOfTwoImage(self):
        "Texture images that have a non-power-of-two dimension should raise an exception."
        self.assertRaises(Exception, pywavefront.texture.Texture, prepend_dir('3x4.png'))

    def testMissingFile(self):
        "Referencing a missing texture file should raise an exception."
        self.assertRaises(Exception, pywavefront.texture.Texture, 'missing.file.do.not.create')
