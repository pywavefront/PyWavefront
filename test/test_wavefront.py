import unittest
import os

import pywavefront

class TestWavefront(unittest.TestCase):
    def setUp(self):
        folder = os.path.dirname(__file__) + '/'
        self.mesh_names = ['Simple', 'SimpleB']
        self.material_names = ['Material.simple', 'Material2.simple']
        self.meshes = pywavefront.Wavefront(folder + 'simple.obj')

    def testMaterials(self):
        "Ensure parsed wavefront materials match known values."
        self.assertEqual(len(self.meshes.materials), len(self.material_names))
        self.assertEqual(self.meshes.materials[self.material_names[0]].__class__,
                        pywavefront.material.Material)

    def testMeshes(self):
        "Ensure parsed wavefront meshes match known values."
        self.assertEqual(len(self.meshes.meshes), len(self.mesh_names))
        self.assertEqual(self.meshes.meshes[self.mesh_names[0]].__class__,
                pywavefront.mesh.Mesh)

    def testMeshList(self):
        "Ensure parsed wavefront mesh list matches known values."
        self.assertEqual(len(self.meshes.mesh_list), len(self.mesh_names))
        self.assertEqual(self.meshes.mesh_list[0].__class__,
                pywavefront.mesh.Mesh)

    def testAddDuplicateMesh(self):
        "Adding a duplicate mesh should increment the mesh list, but not the meshes hash."
        self.meshes.add_mesh(self.meshes.meshes[self.mesh_names[0]])
        self.assertEqual(len(self.meshes.meshes), len(self.mesh_names))
        self.assertEqual(len(self.meshes.mesh_list), len(self.mesh_names) + 1)

    def testMeshMaterialVertices(self):
        "Mesh vertices should have known values."
        self.assertEqual(len(self.meshes.meshes[self.mesh_names[0]].materials[0].vertices), 24)

class TestBrokenWavefront(unittest.TestCase):
    def setUp(self):
        self.folder = os.path.dirname(__file__) + '/'

    def testUnknownUsemtl(self):
        "Referencing an unknown material with usemtl should raise an exception."
        self.assertRaises(pywavefront.PywavefrontException,
                pywavefront.Wavefront, self.folder + 'simple_unknown_usemtl.obj')

    def testMissingNormals(self):
        "If there are texture coordinates but no normals, should raise an exception."
        self.assertRaises(pywavefront.PywavefrontException,
                pywavefront.Wavefront, self.folder + 'simple_missing_normals.obj')

class TestNoMaterial(TestWavefront):
    def setUp(self):
        folder = os.path.dirname(__file__) + '/'
        # reset the obj file to new file with no mtl line
        self.mesh_names = ['Simple', 'SimpleB']
        self.material_names = [None]
        self.meshes = pywavefront.Wavefront(folder + 'simple_no_mtl.obj')

    def testMeshMaterialVertices(self):
        "Mesh vertices should have known values."
        self.assertEqual(len(self.meshes.meshes[self.mesh_names[0]].materials[0].vertices), 48)

class TestNoObjectNoMaterial(TestNoMaterial):
    def setUp(self):
        folder = os.path.dirname(__file__) + '/'

        # reset the obj file to new file with no mtl line
        self.mesh_names = [None]
        self.material_names = [None]
        self.meshes = pywavefront.Wavefront(folder + 'simple_no_object_no_mtl.obj')
