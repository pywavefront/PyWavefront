import unittest
import os

import pywavefront.parser

def prepend_dir(file):
    return os.path.join(os.path.dirname(__file__), file)

class TestParsers(unittest.TestCase):
    def setUp(self):
        # Append current path to locate files
        meshes = pywavefront.Wavefront(prepend_dir('simple.obj'))
        self.mesh1 = meshes.mesh_list[0]
        self.mesh2 = meshes.mesh_list[1]

    def testObjName(self):
        "Parsing an obj file with known names should set those names."
        self.assertEqual(self.mesh1.name, 'Simple')
        self.assertEqual(self.mesh2.name, 'SimpleB')

    def testObjVertices(self):
        "Parsing an obj file with known vertices should set those vertices."
        # tests v, vt, vn, and f
        material = self.mesh1.materials[0]
        self.assertEqual(material.vertices, [
                14.0, 15.0, 20.0, 21.0, 22.0, 0.04, 0.05, 0.06,
                12.0, 13.0, 20.0, 21.0, 22.0, 0.01, 0.02, 0.03,
                10.0, 11.0, 20.0, 21.0, 22.0, 0.07, 0.08, 0.09])
        # One parser vertex comparison is quite enough, thank you!

    def testObjMaterials(self):
        "Parsing an obj file with known materials should load and assign materials."
        # tests mtllib and usemtl
        material1 = self.mesh1.materials[0]
        material2 = self.mesh2.materials[0]
        self.assertEqual(material1.name, 'Material.simple')
        self.assertEqual(material2.name, 'Material2.simple')

class TestMtlParser(unittest.TestCase):
    def setUp(self):
        # Append current path to locate files
        meshes = pywavefront.Wavefront(prepend_dir('simple.obj'))
        self.material1 = meshes.mesh_list[0].materials[0]
        self.material2 = meshes.mesh_list[1].materials[0]

    def testMtlName(self):
        "Parsing an obj file with known material names should set those names."
        self.assertEqual(self.material1.name, 'Material.simple')
        self.assertEqual(self.material2.name, 'Material2.simple')

    def testMtlShininess(self):
        "Parsing an obj file with known material shininess should set it."
        self.assertEqual(self.material1.shininess, 1.0)

    def testMtlAmbient(self):
        "Parsing an obj file with known material ambient should set it."
        # also tests d
        self.assertEqual(self.material1.ambient, [0., 0., 0., 1.])

    def testMtlDiffuse(self):
        "Parsing an obj file with known material diffuse should set it."
        # also tests d
        self.assertEqual(self.material1.diffuse, [0.1, 0.1, 0.1, 1.])

    def testMtlSpecular(self):
        "Parsing an obj file with known material specular should set it."
        # also tests d
        self.assertEqual(self.material1.specular, [0.2, 0.2, 0.2, 1.])

    def testMtlTextureName(self):
        "Parsing an obj file with known material texture should set its name."
        # also tests d
        self.assertEqual(self.material1.texture.image_name,
                         prepend_dir('4x4.png'))

class TestParserFailure(unittest.TestCase):

    def testMissingParseFunction(self):
        "Attempting to parse with a missing parse function should raise an exception."
        # since no parse functions have been defined, this will always fail
        self.assertRaises(Exception, pywavefront.parser.Parser, prepend_dir('uv_sphere.obj'))

    def testMissingParsedFile(self):
        "Referencing a missing parsed file should raise an exception."
        self.assertRaises(Exception, pywavefront.parser.Parser, 'missing.file.do.not.create')
