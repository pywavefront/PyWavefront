import os
import unittest

import pywavefront.parser
from pywavefront.exceptions import PywavefrontException
from pywavefront.material import MaterialParser

def prepend_dir(file):
    return os.path.join(os.path.dirname(__file__), file)


class TestParsers(unittest.TestCase):
    def setUp(self):
        # Append current path to locate files
        meshes = pywavefront.Wavefront(prepend_dir('simple.obj'))
        self.mesh1 = meshes.mesh_list[0]
        self.mesh2 = meshes.mesh_list[1]

    def testObjName(self):
        """Parsing an obj file with known names should set those names."""
        self.assertEqual(self.mesh1.name, 'Simple')
        self.assertEqual(self.mesh2.name, 'SimpleB')

    def testObjVertices(self):
        """Parsing an obj file with known vertices should set those vertices."""
        # tests v, vt, vn, and f
        self.assertEqual(self.mesh1.materials[0].vertices, [
            14.0, 15.0, 20.0, 21.0, 22.0, 0.04, 0.05, 0.06,
            12.0, 13.0, 20.0, 21.0, 22.0, 0.01, 0.02, 0.03,
            10.0, 11.0, 20.0, 21.0, 22.0, 0.07, 0.08, 0.09])

        self.assertEqual(self.mesh2.materials[0].vertices, [
            1.0, 0.0, 0.0, 1.0, -0.0, -1.0, 0.0, 1.0,
            0.0, 0.0, 0.0, 1.0, -0.0, 1.0, 0.0, 1.0,
            0.0, 1.0, 0.0, 1.0, -0.0, 1.0, 0.0, -1.0])

        self.assertEqual(self.mesh2.materials[0].vertex_format, "T2F_N3F_V3F")

    def testObjMaterials(self):
        """Parsing an obj file with known materials should load and assign materials."""
        # tests mtllib and usemtl
        material1 = self.mesh1.materials[0]
        material2 = self.mesh2.materials[0]
        self.assertEqual(material1.name, 'Material.simple')
        self.assertEqual(material2.name, 'Material2.simple')

class NegativeIndices(TestParsers):
    """Run all tests with negative indices"""
    def setUp(self):
        # Append current path to locate files
        meshes = pywavefront.Wavefront(prepend_dir('simple_negative_indices.obj'))
        self.mesh1 = meshes.mesh_list[0]
        self.mesh2 = meshes.mesh_list[1]


class TestParserGz(TestParsers):
    """Run all tests is TestParsers for gzip file as well"""
    def setUp(self):
        # Append current path to locate files
        meshes = pywavefront.Wavefront(prepend_dir('simple.obj.gz'))
        self.mesh1 = meshes.mesh_list[0]
        self.mesh2 = meshes.mesh_list[1]


class TestParserMissingMaterials(unittest.TestCase):
    """Test `create_materials` functionality"""

    def test_missing_material_error(self):
        """Parser should crash if `create_materials` is not set"""
        with self.assertRaises(IOError):
            pywavefront.Wavefront(prepend_dir('simple_missing_material.obj'))

    def test_missing_material_create(self):
        """Parser should handle missing materials if `create_materials` is set"""
        pywavefront.Wavefront(prepend_dir('simple_missing_material.obj'), create_materials=True)


class TestParserVertexVariants(unittest.TestCase):

    def testObjNoNormals(self):
        """Parse obj without normals"""
        # tests v, vt and f
        meshes = pywavefront.Wavefront(prepend_dir('simple_vt.obj'))
        self.mesh1 = meshes.mesh_list[0]
        self.mesh2 = meshes.mesh_list[1]

        self.assertEqual(self.mesh1.materials[0].vertices, [
            14.0, 15.0, 0.04, 0.05, 0.06,
            12.0, 13.0, 0.01, 0.02, 0.03,
            10.0, 11.0, 0.07, 0.08, 0.09])

        self.assertEqual(self.mesh2.materials[0].vertices, [
            1.0, 0.0, -1.0, 0.0, 1.0,
            0.0, 0.0, 1.0, 0.0, 1.0,
            0.0, 1.0, 1.0, 0.0, -1.0])

        self.assertEqual(self.mesh2.materials[0].vertex_format, "T2F_V3F")

    def testObjNoUVs(self):
        """Parse object with no uvs"""
        meshes = pywavefront.Wavefront(prepend_dir('simple_normals.obj'))
        self.mesh1 = meshes.mesh_list[0]
        self.mesh2 = meshes.mesh_list[1]

        self.assertEqual(self.mesh1.materials[0].vertices, [
            20.0, 21.0, 22.0, 0.04, 0.05, 0.06,
            20.0, 21.0, 22.0, 0.01, 0.02, 0.03,
            20.0, 21.0, 22.0, 0.07, 0.08, 0.09])

        self.assertEqual(self.mesh2.materials[0].vertices, [
            0.0, 1.0, -0.0, -1.0, 0.0, 1.0,
            0.0, 1.0, -0.0, 1.0, 0.0, 1.0,
            0.0, 1.0, -0.0, 1.0, 0.0, -1.0])

        self.assertEqual(self.mesh2.materials[0].vertex_format, "N3F_V3F")

    def testObjOnlyPositions(self):
        meshes = pywavefront.Wavefront(prepend_dir('simple_positions.obj'))
        self.mesh1 = meshes.mesh_list[0]
        self.mesh2 = meshes.mesh_list[1]

        self.assertEqual(self.mesh1.materials[0].vertices, [
            0.04, 0.05, 0.06,
            0.01, 0.02, 0.03,
            0.07, 0.08, 0.09])

        self.assertEqual(self.mesh2.materials[0].vertices, [
            -1.0, 0.0, 1.0,
            1.0, 0.0, 1.0,
            1.0, 0.0, -1.0])

        self.assertEqual(self.mesh2.materials[0].vertex_format, "V3F")

    def testObjColors(self):
        meshes = pywavefront.Wavefront(prepend_dir('simple_colors.obj'))
        self.mesh1 = meshes.mesh_list[0]
        self.mesh2 = meshes.mesh_list[1]

        self.assertEqual(self.mesh1.materials[0].vertices, [
            14.0, 15.0, 1.0, 0.0, 0.0, 20.0, 21.0, 22.0, 0.04, 0.05, 0.06,
            12.0, 13.0, 1.0, 0.0, 0.0, 20.0, 21.0, 22.0, 0.01, 0.02, 0.03,
            10.0, 11.0, 1.0, 0.0, 0.0, 20.0, 21.0, 22.0, 0.07, 0.08, 0.09])

        self.assertEqual(self.mesh2.materials[0].vertices, [
            1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, -0.0, -1.0, 0.0, 1.0,
            0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, -0.0, 1.0, 0.0, 1.0,
            0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, -0.0, 1.0, 0.0, -1.0])

        self.assertEqual(self.mesh2.materials[0].vertex_format, "T2F_C3F_N3F_V3F")


class TestMtlParser(unittest.TestCase):
    def setUp(self):
        parser = MaterialParser(prepend_dir('simple_parsetest.mtl'))
        self.materials = parser.materials
        self.material1 = self.materials['Material.simple']
        self.material2 = self.materials['Material2.simple']

    def testMtlName(self):
        """Parsing an obj file with known material names should set those names."""
        self.assertIn('Material.simple', self.materials.keys())
        self.assertIn('Material2.simple', self.materials.keys())

    def testMtlShininess(self):
        """Parsing an obj file with known material shininess should set it."""
        self.assertEqual(self.material1.shininess, 1.0)

    def testMtlAmbient(self):
        """Parsing an obj file with known material ambient should set it."""
        # also tests d
        self.assertEqual(self.material1.ambient, [0., 0., 0., 1.])

    def testMtlDiffuse(self):
        """Parsing an obj file with known material diffuse should set it."""
        # also tests d
        self.assertEqual(self.material1.diffuse, [0.1, 0.1, 0.1, 1.])

    def testMtlSpecular(self):
        """Parsing an obj file with known material specular should set it."""
        # also tests d
        self.assertEqual(self.material1.specular, [0.2, 0.2, 0.2, 1.])

    def testMtlTransparency(self):
        self.assertEqual(self.material1.transparency, 1.0)

    def testMtlIllum(self):
        self.assertEqual(self.material1.illumination_model, 2)

    def testMtlNi(self):
        self.assertEqual(self.material1.optical_density, 0.75)

    def testTextures(self):
        self.assertEqual(self.material1.texture.path, prepend_dir('kd.png'))
        self.assertEqual(self.material1.texture_ambient.path, prepend_dir('ka.png'))
        self.assertEqual(self.material1.texture_specular_color.path, prepend_dir('ks.png'))
        self.assertEqual(self.material1.texture_specular_highlight.path, prepend_dir('ns.png'))
        self.assertEqual(self.material1.texture_alpha.path, prepend_dir('d.png'))
        self.assertEqual(self.material1.texture_bump.path, prepend_dir('bump.png'))


class TestParserFailure(unittest.TestCase):

    def testMissingParseFunction(self):
        """Attempting to parse with a missing parse function should raise an exception."""
        # since no parse functions have been defined, this will always fail in strict mode
        parser = pywavefront.parser.Parser(prepend_dir('simple.obj'), strict=True)
        self.assertRaises(PywavefrontException, parser.parse)

    def testMissingParsedFile(self):
        """Attempting to read a non-exiting file should raise an exception."""
        file_name = 'doesnotexist.obj'
        parser = pywavefront.parser.Parser(prepend_dir(file_name))
        self.assertRaises(IOError, parser.parse)
