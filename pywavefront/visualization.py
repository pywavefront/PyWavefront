# ----------------------------------------------------------------------------
# PyWavefront
# Copyright (c) 2018 Kurt Yoder
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

from pyglet.gl import *

from pywavefront.material import Material
from pywavefront.mesh import Mesh
from pywavefront.texture import Texture

class _Material(object):
    """
    Overrides the drawing routines for the Material class.
    This class should not be used directly. Its purpose is to shadow
    the methods to be overriden.
    """

    def gl_light(self, lighting):
        """Return a GLfloat with length 4, containing the 4 lighting values."""
        return (GLfloat * 4)(*(lighting))

    def draw(self, face=GL_FRONT_AND_BACK):
        if self.texture:
            self.texture.draw()
        else:
            glDisable(GL_TEXTURE_2D)

        glMaterialfv(face, GL_DIFFUSE, self.gl_light(self.diffuse))
        glMaterialfv(face, GL_AMBIENT, self.gl_light(self.ambient))
        glMaterialfv(face, GL_SPECULAR, self.gl_light(self.specular))
        glMaterialfv(face, GL_EMISSION, self.gl_light(self.emissive))
        glMaterialf(face, GL_SHININESS, self.shininess)

        if self.gl_floats is None:
            self.gl_floats = (GLfloat * len(self.vertices))(*self.vertices)
            self.triangle_count = len(self.vertices) / 8
        glInterleavedArrays(GL_T2F_N3F_V3F, 0, self.gl_floats)
        glDrawArrays(GL_TRIANGLES, 0, int(self.triangle_count))


setattr(Material, "gl_light", _Material.gl_light)
setattr(Material, "draw", _Material.draw)


class _Mesh(object):
    """
    Overrides the drawing routines for the Mesh class.
    This class should not be used directly. Its purpose is to shadow
    the methods to be overriden.
    """
    def draw(self):
        glPushClientAttrib(GL_CLIENT_VERTEX_ARRAY_BIT)
        glPushAttrib(GL_CURRENT_BIT | GL_ENABLE_BIT | GL_LIGHTING_BIT)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        for material in self.materials:
            material.draw()
        glPopAttrib()
        glPopClientAttrib()

setattr(Mesh, "draw", _Mesh.draw)


class _Texture(object):

    def init(self, path):
        self.image_name = path
        self.load_image()

    def draw(self):
        if not self.image:
            self.load_image()

        glEnable(self.image.target)
        glBindTexture(self.image.target, self.image.id)
        gl.glTexParameterf(self.image.target,
                           gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP)
        gl.glTexParameterf(self.image.target,
                           gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP)

    def load_image(self):
        self.image = pyglet.image.load(self.image_name).texture
        self.verify_dimensions()

setattr(Texture, "__init__", _Texture.init)
setattr(Texture, "draw", _Texture.draw)
setattr(Texture, "load_image", _Texture.load_image)
