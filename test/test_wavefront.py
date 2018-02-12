import unittest

import pyglet

import pywavefront

class TestWavefront(unittest.TestCase):
    def setUp(self):
        pyglet.resource.path.append('@' + __name__)
        pyglet.resource.reindex()
        self.meshes = pywavefront.Wavefront('simple.obj')

    def testMaterials(self):
        "Ensure parsed wavefront materials match known values."
        self.assertEqual(len(self.meshes.materials), 2)
        self.assertEqual(self.meshes.materials['Material.simple'].__class__,
                pywavefront.material.Material)

    def testMeshes(self):
        "Ensure parsed wavefront meshes match known values."
        self.assertEqual(len(self.meshes.meshes), 2)
        self.assertEqual(self.meshes.meshes['Simple'].__class__,
                pywavefront.mesh.Mesh)

    def testMeshList(self):
        "Ensure parsed wavefront mesh list matches known values."
        self.assertEqual(len(self.meshes.mesh_list), 2)
        self.assertEqual(self.meshes.mesh_list[0].__class__,
                pywavefront.mesh.Mesh)

    def testAddDuplicateMesh(self):
        "Adding a duplicate mesh should increment the mesh list, but not the meshes hash."
        self.meshes.add_mesh(self.meshes.meshes['Simple'])
        self.assertEqual(len(self.meshes.meshes), 2)
        self.assertEqual(len(self.meshes.mesh_list), 3)

    def testMeshMaterialVertices(self):
        "Mesh vertices should have known values."
        self.assertEqual(len(self.meshes.meshes['Simple'].materials[0].vertices), 24)

class TestBrokenWavefront(unittest.TestCase):
    def setUp(self):
        pyglet.resource.path.append('@' + __name__)
        pyglet.resource.reindex()

    def testUnknownUsemtl(self):
        "Referencing an unknown material with usemtl should raise an exception."
        self.assertRaises(pywavefront.PywavefrontException,
                pywavefront.Wavefront, 'simple_unknown_usemtl.obj')

    def testMissingNormals(self):
        "If there are texture coordinates but no normals, should raise an exception."
        self.assertRaises(pywavefront.PywavefrontException,
                pywavefront.Wavefront, 'simple_missing_normals.obj')

class TestNoMaterial(TestWavefront):
    def setUp(self):
        pyglet.resource.path.append('@' + __name__)
        pyglet.resource.reindex()
        # reset the obj file to new file with no mtl line
        self.meshes = pywavefront.Wavefront('simple_no_mtl.obj')

    def testMaterials(self):
        """Override this test"""
        pass

    def testMeshMaterialVertices(self):
        "Mesh vertices should have known values."
        self.assertEqual(len(self.meshes.meshes['Simple'].materials[0].vertices), 48)
