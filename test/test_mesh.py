import unittest

import pywavefront.mesh

class TestMesh(unittest.TestCase):

    def testMeshName(self):
        "Creating a mesh with a name should set the name."
        my_mesh = pywavefront.mesh.Mesh('qax')
        self.assertEqual(my_mesh.name, 'qax')

