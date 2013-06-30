"""This module imports Wavefront-formatted 3D object definitions and
converts them into pyglet vertex lists."""

# Derived from `contrib/model/examples/obj_test.py` in the pyglet directory
from pyglet.gl import *

import material
import mesh
import parser

class PywavefrontException(Exception):
    pass

class Wavefront(object):
    """Import a wavefront .obj file."""
    def __init__(self, file_name, path=None):
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
        if not the_mesh.name: return
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
        self.vertices.append(map(float, args[0:3]))

    def parse_vn(self, args):
        self.normals.append(map(float, args[0:3]))

    def parse_vt(self, args):
        self.tex_coords.append(map(float, args[0:2]))

    def parse_mtllib(self, args):
        [mtllib] = args
        materials = material.MaterialParser(mtllib).materials
        for material_name, material_object in materials.iteritems():
            self.wavefront.materials[material_name] = material_object

    def parse_usemtl(self, args):
        [usemtl] = args
        self.material = self.wavefront.materials.get(usemtl, None)
        if self.material is None:
            raise PywavefrontException, 'Unknown material: %s' % args[0]
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
            raise PywavefrontException, 'Found texture coordinates, but no normals'

        if self.mesh is None:
            self.mesh = mesh.Mesh()
            self.wavefront.add_mesh(self.mesh)
        if self.material is None:
            self.material = material.Material()
        self.mesh.add_material(self.material)

        # For fan triangulation, remember first and latest vertices
        v1 = None
        vlast = None
        points = []
        for i, v in enumerate(args[0:]):
            v_index, t_index, n_index = \
                (map(int, [j or 0 for j in v.split('/')]) + [0, 0])[:3]
            if v_index < 0:
                v_index += len(self.vertices) - 1
            if t_index < 0:
                t_index += len(self.tex_coords) - 1
            if n_index < 0:
                n_index += len(self.normals) - 1
            vertex = self.tex_coords[t_index] + \
                     self.normals[n_index] + \
                     self.vertices[v_index] 

            if i >= 3:
                # Triangulate
                self.material.vertices += v1 + vlast
            self.material.vertices += vertex

            if i == 0:
                v1 = vertex
            vlast = vertex

    def parse_s(self, args):
        # don't know what this does
        return
