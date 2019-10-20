import os
import unittest

import pywavefront.parser
from pywavefront.exceptions import PywavefrontException
from pywavefront.material import MaterialParser

from utils import fixture


class TestParsers(unittest.TestCase):

    def setUp(self):
        # Append current path to locate files
        meshes = pywavefront.Wavefront(fixture('simple.obj'))
        self.mesh1 = meshes.mesh_list[0]
        self.mesh2 = meshes.mesh_list[1]
        self.maxDiff = None

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


class TestParserCollectFaces(unittest.TestCase):
    """Test collecting (possibly triangulated) faces"""
    def setUp(self):
        self.meshes = pywavefront.Wavefront(fixture('arbitrary-faces.obj'), collect_faces=True).meshes

    def testTrianglesOnlyFaces(self):
        self.assertTrue(self.meshes['triangleOnly'].has_faces)
        self.assertEqual(self.meshes['triangleOnly'].faces, [[1, 0, 2]])

    def testQuadFaces(self):
        self.assertTrue(self.meshes['quadOnly'].has_faces)
        self.assertEqual(self.meshes['quadOnly'].faces, [
            [4, 5, 6], [7, 4, 6],
            [5, 4, 6], [7, 5, 6],
            [7, 6, 4], [5, 7, 4]
        ])

    def testArbitrarilyMixedFaced(self):
        self.assertTrue(self.meshes['arbitrary'].has_faces)
        self.assertEqual(self.meshes['arbitrary'].faces, [
            [8, 9, 10], [11, 8, 10],
            [11, 8, 9], [10, 11, 9], [12, 11, 10],
            [12, 9, 10], [8, 12, 10], [11, 12, 8], [13, 12, 11],
            [13, 11, 9]
        ])


class NegativeIndices(TestParsers):
    """Run all tests with negative indices"""
    def setUp(self):
        # Append current path to locate files
        meshes = pywavefront.Wavefront(fixture('simple_negative_indices.obj'))
        self.mesh1 = meshes.mesh_list[0]
        self.mesh2 = meshes.mesh_list[1]


class TestParserGz(TestParsers):
    """Run all tests is TestParsers for gzip file as well"""
    def setUp(self):
        # Append current path to locate files
        meshes = pywavefront.Wavefront(fixture('simple.obj.gz'))
        self.mesh1 = meshes.mesh_list[0]
        self.mesh2 = meshes.mesh_list[1]


class TestParserMissingMaterials(unittest.TestCase):
    """Test `create_materials` functionality"""

    def test_missing_material_error(self):
        """Parser should crash if `create_materials` is not set"""
        with self.assertRaises(IOError):
            pywavefront.Wavefront(fixture('simple_missing_material.obj'))

    def test_missing_material_create(self):
        """Parser should handle missing materials if `create_materials` is set"""
        pywavefront.Wavefront(fixture('simple_missing_material.obj'), create_materials=True)


class TestParserVertexVariants(unittest.TestCase):
    maxDiff = None

    def testObjNoNormals(self):
        """Parse obj without normals"""
        # tests v, vt and f
        meshes = pywavefront.Wavefront(fixture('simple_vt.obj'))
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
        meshes = pywavefront.Wavefront(fixture('simple_normals.obj'))
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
        meshes = pywavefront.Wavefront(fixture('simple_positions.obj'))
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
        meshes = pywavefront.Wavefront(fixture('simple_colors.obj'))
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

    def test_undefined_uvs(self):
        """obj file were some uv entries are undefiend"""
        meshes = pywavefront.Wavefront(fixture('simple_missing_uv.obj'))
        self.mesh2 = meshes.mesh_list[1]

        self.assertEqual(self.mesh2.materials[0].vertices, [
            1.0, 0.0, 0.0, 1.0, -0.0, -1.0, 0.0, 1.0,
            0.0, 0.0, 0.0, 1.0, -0.0, 1.0, 0.0, 1.0,
            0.0, 1.0, 0.0, 1.0, -0.0, 1.0, 0.0, -1.0,

            10.0, 11.0, 0.0, 1.0, -0.0, -1.0, 0.0, 1.0,
            10.0, 11.0, 0.0, 1.0, -0.0, 1.0, 0.0, 1.0,
            10.0, 11.0, 0.0, 1.0, -0.0, 1.0, 0.0, -1.0,

            1.0, 0.0, 0.0, 1.0, -0.0, -1.0, 0.0, 1.0,
            0.0, 0.0, 0.0, 1.0, -0.0, 1.0, 0.0, 1.0,
            0.0, 1.0, 0.0, 1.0, -0.0, 1.0, 0.0, -1.0,
        ])

        self.assertEqual(self.mesh2.materials[0].vertex_format, "T2F_N3F_V3F")


class TestMtlParser(unittest.TestCase):
    def setUp(self):
        parser = MaterialParser(fixture('simple_parsetest.mtl'), strict=True)
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
        self.assertEqual(self.material1.texture.path, str(fixture('kd.png')))
        self.assertEqual(self.material1.texture.name, 'kd.png')
        self.assertEqual(self.material1.texture_ambient.path, str(fixture('ka.png')))
        self.assertEqual(self.material1.texture_ambient.name, 'ka.png')
        self.assertEqual(self.material1.texture_specular_color.path, str(fixture('ks.png')))
        self.assertEqual(self.material1.texture_specular_color.name, 'ks.png')
        self.assertEqual(self.material1.texture_specular_highlight.path, str(fixture('ns.png')))
        self.assertEqual(self.material1.texture_specular_highlight.name, 'ns.png')
        self.assertEqual(self.material1.texture_alpha.path, str(fixture('d.png')))
        self.assertEqual(self.material1.texture_alpha.name, 'd.png')
        self.assertEqual(self.material1.texture_bump.path, str(fixture('bump.png')))
        self.assertEqual(self.material1.texture_bump.name, 'bump.png')


class TestParserFailure(unittest.TestCase):

    def testMissingParseFunction(self):
        """Attempting to parse with a missing parse function should raise an exception."""
        # since no parse functions have been defined, this will always fail in strict mode
        parser = pywavefront.parser.Parser(fixture('simple.obj'), strict=True)
        self.assertRaises(PywavefrontException, parser.parse)

    def testMissingParsedFile(self):
        """Attempting to read a non-exiting file should raise an exception."""
        file_name = 'doesnotexist.obj'
        with self.assertRaises(IOError):
            parser = pywavefront.parser.Parser(fixture(file_name))
            parser.parse()
