import warnings

from pyglet.gl import *

import parser
import texture

class Material(object):
    # set defaults
    diffuse = [.8, .8, .8]
    ambient = [.2, .2, .2]
    specular = [0., 0., 0.]
    emission = [0., 0., 0.]
    shininess = 0.
    opacity = 1.
    texture = None

    def __init__(self, name):
        self.name = name

        # Interleaved array of floats in GL_T2F_N3F_V3F format
        self.vertices = []
        self.gl_floats = None

    def set_texture(self, path):
        self.texture = texture.Texture(path)

    def gl_light(self, lighting):
        """Return a GLfloat with length 4, containing the 3 lighting values and
        appending opacity."""
        return (GLfloat * 4)(*(lighting + [self.opacity]))

    def draw(self, face=GL_FRONT_AND_BACK):
        if self.texture:
            self.texture.draw()
        else:
            glDisable(GL_TEXTURE_2D)

        glMaterialfv(face, GL_DIFFUSE, self.gl_light(self.diffuse) )
        glMaterialfv(face, GL_AMBIENT, self.gl_light(self.ambient) )
        glMaterialfv(face, GL_SPECULAR, self.gl_light(self.specular) )
        glMaterialfv(face, GL_EMISSION, self.gl_light(self.emission) )
        glMaterialf(face, GL_SHININESS, self.shininess)

        if self.gl_floats is None:
            self.gl_floats = (GLfloat * len(self.vertices))(*self.vertices)
            self.triangle_count = len(self.vertices) / 8
        glInterleavedArrays(GL_T2F_N3F_V3F, 0, self.gl_floats)
        glDrawArrays(GL_TRIANGLES, 0, self.triangle_count)

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
        self.this_material.diffuse = map(float, args[0:])

    def parse_Ka(self, args):
        self.this_material.ambient = map(float, args[0:])

    def parse_Ks(self, args):
        self.this_material.specular = map(float, args[0:])

    def parse_Ke(self, args):
        self.this_material.emissive = map(float, args[0:])

    def parse_Ns(self, args):
        [Ns] = args
        self.this_material.shininess = float(Ns)

    def parse_d(self, args):
        [d] = args
        self.this_material.opacity = float(d)

    def parse_map_Kd(self, args):
        [Kd] = args
        self.this_material.set_texture(Kd)

    def parse_Ni(self, args):
        # don't know what this does
        return

    def parse_illum(self, args):
        # don't know what this does
        return
