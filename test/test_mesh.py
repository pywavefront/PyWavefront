import unittest

import pyglet

import pywavefront.mesh

class TestMesh(unittest.TestCase):
    def setUp(self):
        pyglet.resource.path.append('@' + __name__)
        pyglet.resource.reindex()

    def testMeshName(self):
        "Creating a mesh with a name should set the name."
        my_mesh = pywavefront.mesh.Mesh('qax')
        self.assertEqual(my_mesh.name, 'qax')

