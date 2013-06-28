import unittest

import pyglet

import pywavefront.parser

class TestParser(unittest.TestCase):

    def testMissingParseFunction(self):
        "Attempting to parse with a missing parse function should raise an exception."
        # since no parse functions have been defined, this will always fail
        pyglet.resource.path.append('@' + __name__)
        pyglet.resource.reindex()
        self.assertRaises(Exception, pywavefront.parser.Parser, 'uv_sphere.obj')
