import unittest
import os

import pywavefront.material

def prepend_dir(file):
    return os.path.join(os.path.dirname(__file__), file)

class TestMaterial(unittest.TestCase):
    def setUp(self):
        # Append current path to locate files
        self.material = pywavefront.material.Material(prepend_dir('material'))
        self.material.set_texture(prepend_dir('4x4.png'))

    def testSetTexture(self):
        "Running set_texture should set a texture."
        self.assertEqual(self.material.texture.__class__,
                pywavefront.texture.Texture)

    def testUnsetTexture(self):
        "Running unset_texture should set texture to None."
        self.material.unset_texture()
        self.assertEqual(self.material.texture, None)

    def testPadLight(self):
        "pad_light should return known values."
        self.assertEqual(self.material.pad_light([1.]),
                [1., 0., 0., 0.])

    def testSetAlpha(self):
        "set_alpha should set known values."
        self.material.set_alpha(0)
        self.assertEqual(self.material.diffuse[3], 0.)
        self.assertEqual(self.material.ambient[3], 0.)
        self.assertEqual(self.material.specular[3], 0.)
        self.assertEqual(self.material.emissive[3], 0.)

    def testSetDiffuse(self):
        "set_diffuse should set known values."
        self.material.set_diffuse([1, 0])
        self.assertEqual(self.material.diffuse, [1., 0., 0., 0.])

    def testSetAmbient(self):
        "set_ambient should set known values."
        self.material.set_ambient([1, 0, 0.5, 0.2])
        self.assertEqual(self.material.ambient, [1., 0., 0.5, 0.2])

    def testSetSpecular(self):
        "set_specular should set known values."
        self.material.set_specular()
        self.assertEqual(self.material.specular, [0., 0., 0., 0.])

    def testSetEmissive(self):
        "set_emissive should set known values."
        self.material.set_emissive()
        self.assertEqual(self.material.emissive, [0., 0., 0., 0.])

class TestInvalidMaterial(unittest.TestCase):

    def testSetInvalidTexture(self):
        "Running set_texture with a nonexistent file should raise an exception."
        material = pywavefront.material.Material('material')
        self.assertRaises(Exception, material.set_texture, 'missing.file.do.not.create')
