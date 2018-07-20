# ----------------------------------------------------------------------------
# PyWavefront
# Copyright (c) 2013 Kurt Yoder
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of PyWavefront nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------
import logging
import os

from pywavefront.parser import Parser, auto_consume
from pywavefront.texture import Texture

logger = logging.getLogger("pywavefront")


class Material(object):
    def __init__(self, name, is_default=False):
        """
        Create a new material
        :param name: Name of the material
        :param is_default: Is this an auto created default material?
        """
        self.name = name
        self.diffuse = [.8, .8, .8, 1.]
        self.ambient = [.2, .2, .2, 1.]
        self.specular = [0., 0., 0., 1.]
        self.emissive = [0., 0., 0., 1.]
        self.shininess = 0.
        self.texture = None
        self.is_default = is_default

        # Interleaved array of floats in GL_T2F_N3F_V3F format
        self.vertex_format = ""
        self.vertices = []

        self.gl_floats = None

    @property
    def file(self):
        """File with full path"""
        return os.path.join(self.path, self.name)

    @property
    def has_normals(self):
        return "N3F" in self.vertex_format

    @property
    def has_uvs(self):
        return "T2F" in self.vertex_format

    @property
    def has_colors(self):
        return "C3F" in self.vertex_format

    @property
    def vertex_size(self):
        """How many float each vertex contains in the interleaved data"""
        return self.has_uvs * 2 + self.has_normals * 3 + self.has_colors * 3 + 3

    def pad_light(self, values):
        """Accept an array of up to 4 values, and return an array of 4 values.
        If the input array is less than length 4, pad it with zeroes until it
        is length 4. Also ensure each value is a float"""
        while len(values) < 4:
            values.append(0.)

        return list(map(float, values))

    def set_alpha(self, alpha):
        """Set alpha/last value on all four lighting attributes."""
        alpha = float(alpha)
        self.diffuse[3] = alpha
        self.ambient[3] = alpha
        self.specular[3] = alpha
        self.emissive[3] = alpha

    def set_diffuse(self, values=None):
        self.diffuse = self.pad_light(values or [])

    def set_ambient(self, values=None):
        self.ambient = self.pad_light(values or [])

    def set_specular(self, values=None):
        self.specular = self.pad_light(values or [])

    def set_emissive(self, values=None):
        self.emissive = self.pad_light(values or [])

    def set_texture(self, path):
        self.texture = Texture(path)

    def unset_texture(self):
        self.texture = None


class MaterialParser(Parser):
    """Object to parse lines of a materials definition file."""

    def __init__(self, file_name, strict=False, encoding="utf-8", parse=True):
        """
        Create a new material parser
        :param file_name: file name and path of obj file to read
        :param strict: Enable strict mode
        :param encoding: Encoding to read the text files
        :param parse: Should parse be called immediately or manually called later?
        """
        super(MaterialParser, self).__init__(file_name, strict=strict, encoding=encoding)

        self.materials = {}
        self.this_material = None

        if parse:
            self.parse()

    @auto_consume
    def parse_newmtl(self):
        self.this_material = Material(self.values[1])
        self.materials[self.this_material.name] = self.this_material

    @auto_consume
    def parse_Kd(self):
        self.this_material.set_diffuse(self.values[1:])

    @auto_consume
    def parse_Ka(self):
        self.this_material.set_ambient(self.values[1:])

    @auto_consume
    def parse_Ks(self):
        self.this_material.set_specular(self.values[1:])

    @auto_consume
    def parse_Ke(self):
        self.this_material.set_emissive(self.values[1:])

    @auto_consume
    def parse_Ns(self):
        self.this_material.shininess = float(self.values[1])

    @auto_consume
    def parse_d(self):
        self.this_material.set_alpha(self.values[1])

    @auto_consume
    def parse_map_Kd(self):
        Kd = os.path.join(self.dir, " ".join(self.values[1:]))
        self.this_material.set_texture(Kd)

    @auto_consume
    def parse_Ni(self):
        # unimplemented
        pass

    @auto_consume
    def parse_Tr(self):
        # unimplemented
        pass

    @auto_consume
    def parse_illum(self):
        # unimplemented
        pass
