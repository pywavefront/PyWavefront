import os

from pywavefront.exceptions import PywavefrontException
from pywavefront.parser import Parser, auto_consume
from pywavefront.material import Material, MaterialParser
from pywavefront.mesh import Mesh


class ObjParser(Parser):
    """This parser parses lines from .obj files."""

    def __init__(self, wavefront, file_name, strict=False, encoding="utf-8", parse=True):
        """
        Create a new obj parser
        :param wavefront: The wavefront object
        :param file_name: file name and path of obj file to read
        :param strict: Enable strict mode
        :param encoding: Encoding to read the text files
        :param parse: Should parse be called immediately or manually called later?
        """
        super(ObjParser, self).__init__(file_name, strict=strict, encoding=encoding)
        self.wavefront = wavefront

        self.mesh = None
        self.material = None
        self.vertices = [[0., 0., 0.]]
        self.normals = [[0., 0., 0.]]
        self.tex_coords = [[0., 0.]]

        if parse:
            self.parse()

    # methods for parsing types of wavefront lines
    def parse_v(self):
        self.vertices += list(self.consume_vertices())

    def consume_vertices(self):
        """
        Consumes all consecutive vertices.
        NOTE: There is no guarantee this will consume all vertices since other
        statements can also occur in the vertex list
        """
        while True:
            # TODO: Check for vertex color
            yield (
                float(self.values[1]),
                float(self.values[2]),
                float(self.values[3]),
            )

            self.next_line()
            if self.values[0] != "v":
                break

    def parse_vn(self):
        self.normals += list(self.consume_normals())

        # Since list() also consumes StopIteration we need to sanity check the line
        # to make sure the parser advances
        if self.values[0] == "vn":
            self.next_line()

    def consume_normals(self):
        """Consumes all consecutive texture coordinate lines"""
        # The first iteration processes the current/first vn statement.
        # The loop continues until there are no more vn-statements or StopIteration is raised by generator
        while True:
            yield (
                float(self.values[1]),
                float(self.values[2]),
                float(self.values[3]),
            )

            self.next_line()
            if self.values[0] != "vn":
                break

    def parse_vt(self):
        self.tex_coords += list(self.consume_texture_coordinates())

        # Since list() also consumes StopIteration we need to sanity check the line
        # to make sure the parser advances
        if self.values[0] == "vt":
            self.next_line()

    def consume_texture_coordinates(self):
        """Consume all consecutive texture coordinates"""
        # The first iteration processes the current/first vt statement.
        # The loop continues until there are no more vt-statements or StopIteration is raised by generator
        while True:
            yield (
                float(self.values[1]),
                float(self.values[2]),
            )

            self.next_line()
            if self.values[0] != "vt":
                break

    @auto_consume
    def parse_mtllib(self):
        mtllib = os.path.join(self.dir, " ".join(self.values[1:]))
        materials = MaterialParser(mtllib, encoding=self.encoding, strict=self.strict).materials

        for material_name, material_object in materials.items():
            self.wavefront.materials[material_name] = material_object

    @auto_consume
    def parse_usemtl(self):
        self.material = self.wavefront.materials.get(self.values[1], None)

        if self.material is None:
            raise PywavefrontException('Unknown material: %s' % self.values[1])

        if self.mesh is not None:
            self.mesh.add_material(self.material)

    def parse_usemat(self):
        self.parse_usemtl()

    @auto_consume
    def parse_o(self):
        self.mesh = Mesh(self.values[1])
        self.wavefront.add_mesh(self.mesh)

    def parse_f(self):
        # Support objects without `o` statement
        if self.mesh is None:
            self.mesh = Mesh()
            self.wavefront.add_mesh(self.mesh)

        # Add default material if not created
        if self.material is None:
            self.material = Material(is_default=True)
            self.wavefront.materials[self.material.name] = self.material

        self.mesh.add_material(self.material)

        self.material.vertices += list(self.consume_faces())

        # Since list() also consumes StopIteration we need to sanity check the line
        # to make sure the parser advances
        if self.values[0] == "f":
            self.next_line()

    def consume_faces(self):
        """
        Consume all consecutive faces

        If a 4th vertex is specified, we triangulate.
        In a perfect world we could consume this straight forward and draw using GL_TRIANGLE_FAN.
        This is however rarely the case..

        * If the face is co-planar but concave, then you need to triangulate the face
        * If the face is not-coplanar, you are screwed, because OBJ doesn't preserve enough information
          to know what tessellation was intended

        We always triangulate to make it simple
        """
        # The first iteration processes the current/first f statement.
        # The loop continues until there are no more f-statements or StopIteration is raised by generator
        while True:
            v1 = None
            vlast = None

            for i, v in enumerate(self.values[1:]):
                v_index, t_index, n_index = (list(map(int, [j or 0 for j in v.split('/')])) + [0, 0])[:3]

                # Resolve negative index lookups
                if v_index < 0:
                    v_index += len(self.vertices) - 1

                if t_index < 0:
                    t_index += len(self.tex_coords) - 1

                if n_index < 0:
                    n_index += len(self.normals) - 1

                vertex = (
                    self.tex_coords[t_index][0],
                    self.tex_coords[t_index][1],

                    self.normals[n_index][0],
                    self.normals[n_index][1],
                    self.normals[n_index][2],

                    self.vertices[v_index][0],
                    self.vertices[v_index][1],
                    self.vertices[v_index][2],
                )

                for v in vertex:
                    yield v

                if i >= 3:
                    # Emit vertex 1 and 3 triangulating when a 4th vertex is specified
                    for v in v1:
                        yield v

                    for v in vlast:
                        yield v

                if i == 0:
                    v1 = vertex

                vlast = vertex

            # Break out of the loop when there are no more f statements
            self.next_line()
            if self.values[0] != "f":
                break
