import unittest

import pyglet

import pywavefront.material

class TestMaterial(unittest.TestCase):
    def setUp(self):
        pyglet.resource.path.append('@' + __name__)
        pyglet.resource.reindex()

    def testSetTexture(self):
        "Running set_texture should set a texture."
        material = pywavefront.material.Material('material')
        material.set_texture('4x4.png')
        self.assertEqual(material.texture.__class__,
                pywavefront.texture.Texture)

    def testSetInvalidTexture(self):
        "Running set_texture with a nonexistent file should raise an exception."
        material = pywavefront.material.Material('material')
        self.assertRaises(Exception, material.set_texture, 'missing.file.do.not.create')
