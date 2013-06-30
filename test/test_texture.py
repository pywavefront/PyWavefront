import unittest

import pyglet

import pywavefront.texture

class TestTexture(unittest.TestCase):
    def setUp(self):
        pyglet.resource.path.append('@' + __name__)
        pyglet.resource.reindex()

    def testPathedImageName(self):
        "For Texture objects, the image name should be the last component of the path."
        my_texture = pywavefront.texture.Texture('foo/bar/4x4.png')
        self.assertEqual(my_texture.image_name, '4x4.png')

    def testNonPowerOfTwoImage(self):
        "Texture images that have a non-power-of-two dimension should raise an exception."
        self.assertRaises(Exception, pywavefront.texture.Texture, '3x4.png')

    def testMissingFile(self):
        "Referencing a missing texture file should raise an exception."
        self.assertRaises(Exception, pywavefront.texture.Texture, 'missing.file.do.not.create')
