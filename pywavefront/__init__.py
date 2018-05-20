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

import pywavefront.material
import pywavefront.mesh
import pywavefront.parser

class PywavefrontException(Exception):
    pass

class Wavefront(object):
    """Import a wavefront .obj file."""
    def __init__(self, file_name):
        self.file_name = file_name

        self.materials = {}
        self.meshes = {}        # Name mapping
        self.mesh_list = []     # Also includes anonymous meshes

        ObjParser(self, self.file_name)

    def draw(self):
        for this_mesh in self.mesh_list:
            this_mesh.draw()

    def add_mesh(self, the_mesh):
        self.mesh_list.append(the_mesh)
        self.meshes[the_mesh.name] = the_mesh

class ObjParser(parser.Parser):
    """This parser parses lines from .obj files."""
    def __init__(self, wavefront, file_name):
        # unfortunately we can't escape from external effects on the
        # wavefront object
        self.wavefront = wavefront
        self.mesh = None
        self.material = None
        self.vertices = [[0., 0., 0.]]
        self.normals = [[0., 0., 0.]]
        self.tex_coords = [[0., 0.]]
        self.read_file(file_name)

    # methods for parsing types of wavefront lines
    def parse_v(self, args):
        self.vertices.append(list(map(float, args[0:3])))

    def parse_vn(self, args):
        self.normals.append(list(map(float, args[0:3])))

    def parse_vt(self, args):
        self.tex_coords.append(list(map(float, args[0:2])))

    def parse_mtllib(self, args):
        [mtllib] = args
        materials = material.MaterialParser(mtllib).materials
        for material_name, material_object in materials.items():
            self.wavefront.materials[material_name] = material_object

    def parse_usemtl(self, args):
        [usemtl] = args
        self.material = self.wavefront.materials.get(usemtl, None)
        if self.material is None:
            raise PywavefrontException('Unknown material: %s' % args[0])
        if self.mesh is not None:
            self.mesh.add_material(self.material)

    def parse_usemat(self, args):
        self.parse_usemtl(args)

    def parse_o(self, args):
        [o] = args
        self.mesh = mesh.Mesh(o)
        self.wavefront.add_mesh(self.mesh)

    def parse_f(self, args):
        if (len(self.tex_coords) > 1) and (len(self.normals) == 1): 
            # does the spec allow for texture coordinates without normals?
            # if we allow this condition, the user will get a black screen
            # which is really confusing
            raise PywavefrontException('Found texture coordinates, but no normals')

        if self.mesh is None:
            self.mesh = mesh.Mesh()
            self.wavefront.add_mesh(self.mesh)
        if self.material is None:
            self.material = material.Material()
            self.wavefront.materials[self.material.name] = self.material
        self.mesh.add_material(self.material)

        # For fan triangulation, remember first and latest vertices
        v1 = None
        vlast = None
        points = []
        for i, v in enumerate(args[0:]):
            if type(v) is bytes:
                v = v.decode()
            v_index, t_index, n_index = \
                (list(map(int, [j or 0 for j in v.split('/')])) + [0, 0])[:3]
            if v_index < 0:
                v_index += len(self.vertices) - 1
            if t_index < 0:
                t_index += len(self.tex_coords) - 1
            if n_index < 0:
                n_index += len(self.normals) - 1
            vertex = list(self.tex_coords[t_index]) + \
                     list(self.normals[n_index]) + \
                     list(self.vertices[v_index]) 

            if i >= 3:
                # Triangulate
                self.material.vertices += v1 + vlast
            self.material.vertices += vertex

            if i == 0:
                v1 = vertex
            vlast = vertex
