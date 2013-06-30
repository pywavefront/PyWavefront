import unittest

import pyglet

import pywavefront.parser

class TestParser(unittest.TestCase):
    def setUp(self):
        pyglet.resource.path.append('@' + __name__)
        pyglet.resource.reindex()

    def testMissingParseFunction(self):
        "Attempting to parse with a missing parse function should raise an exception."
        # since no parse functions have been defined, this will always fail
        self.assertRaises(Exception, pywavefront.parser.Parser, 'uv_sphere.obj')

    def testMissingParsedFile(self):
        "Referencing a missing parsed file should raise an exception."
        self.assertRaises(Exception, pywavefront.parser.Parser, 'missing.file.do.not.create')
