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

from pyglet.gl import *

class Texture(object):
    def __init__(self, path):
        # wavefront file has relative paths
        # we only need the file name, since pyglet takes care of path lookups
        self.image_name = path.split('/')[-1]

        self.image = pyglet.resource.image(self.image_name).texture

        self.verify_dimensions()

    def draw(self):
        glEnable(self.image.target)
        glBindTexture(self.image.target, self.image.id)
        gl.glTexParameterf(self.image.target,
                gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP)
        gl.glTexParameterf(self.image.target,
                gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP)

    def verify_dimensions(self):
        self.verify('width')
        self.verify('height')

    def verify(self, dimension):
        value = self.image.__getattribute__(dimension)
        while value > 1:
            div_float = float(value) / 2.0
            div_int = int(div_float)
            if not (div_float == div_int):
                raise Exception( 'image %s is %d, which is not a power of 2'%(
                        dimension, self.image.__getattribute__(dimension) ))
            value = div_int

