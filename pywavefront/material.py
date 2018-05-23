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

import pywavefront.parser as parser
import pywavefront.texture as texture


class Material(object):
    def __init__(self, name=None):
        self.name = name
        self.diffuse = [.8, .8, .8, 1.]
        self.ambient = [.2, .2, .2, 1.]
        self.specular = [0., 0., 0., 1.]
        self.emissive = [0., 0., 0., 1.]
        self.shininess = 0.
        self.texture = None

        # Interleaved array of floats in GL_T2F_N3F_V3F format
        self.vertices = []
        self.gl_floats = None

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

    def set_diffuse(self, values=[]):
        self.diffuse = self.pad_light(values)

    def set_ambient(self, values=[]):
        self.ambient = self.pad_light(values)

    def set_specular(self, values=[]):
        self.specular = self.pad_light(values)

    def set_emissive(self, values=[]):
        self.emissive = self.pad_light(values)

    def set_texture(self, path):
        self.texture = texture.Texture(path)

    def unset_texture(self):
        self.texture = None

    def gl_light(self, lighting):
        """Method placeholder"""
        raise Exception("Please import pywavefront.visualization")

    def draw(self, face=None):
        """Method placeholder"""
        raise Exception("Please import pywavefront.visualization")


class MaterialParser(parser.Parser):
    """Object to parse lines of a materials definition file."""

    def __init__(self, file_path):
        self.materials = {}
        self.this_material = None
        self.read_file(file_path)

    def parse_newmtl(self, args):
        [newmtl] = args
        self.this_material = Material(newmtl)
        self.materials[self.this_material.name] = self.this_material

    def parse_Kd(self, args):
        self.this_material.set_diffuse(args)

    def parse_Ka(self, args):
        self.this_material.set_ambient(args)

    def parse_Ks(self, args):
        self.this_material.set_specular(args)

    def parse_Ke(self, args):
        self.this_material.set_emissive(args)

    def parse_Ns(self, args):
        [Ns] = args
        self.this_material.shininess = float(Ns)

    def parse_d(self, args):
        [d] = args
        self.this_material.set_alpha(d)

    def parse_map_Kd(self, args):
        [Kd] = args
        self.this_material.set_texture(Kd)

    def parse_Ni(self, args):
        # unimplemented
        return

    def parse_Tr(self, args):
        # unimplemented
        return

    def parse_illum(self, args):
        # unimplemented
        return
