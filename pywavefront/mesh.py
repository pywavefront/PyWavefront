from pyglet.gl import *

class Mesh(object):
    """This is a basic mesh for drawing using OpenGL. Interestingly, it does
    not contain its own vertices. These are instead drawn via materials."""

    def __init__(self, name=''):
        self.name = name
        self.materials = []

    def has_material(self, new_material):
        """Determine whether we already have a material of this name."""
        for material in self.materials:
            if material.name == new_material.name: return True
        return False

    def add_material(self, material):
        """Add a material to the mesh, IFF it is not already present."""
        if self.has_material(material): return
        self.materials.append(material)

    def draw(self):
        glPushClientAttrib(GL_CLIENT_VERTEX_ARRAY_BIT)
        glPushAttrib(GL_CURRENT_BIT | GL_ENABLE_BIT | GL_LIGHTING_BIT)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        for material in self.materials:
            material.draw()
        glPopAttrib()
        glPopClientAttrib()
