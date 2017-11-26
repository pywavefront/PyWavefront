import unittest

import pyglet

import pywavefront.parser


class TestParsingLightwave(unittest.TestCase):

    def setUp(self):
        pyglet.resource.path.append('@' + __name__)
        pyglet.resource.reindex()
        self.meshes = pywavefront.Wavefront('lightwave_style.obj')

    def test_parsing_lightwave_group_name(self):
        self.assertEqual(self.meshes.mesh_list[0].group, "Default")
