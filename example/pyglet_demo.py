#!/usr/bin/env python
"""This script shows an example of using the PyWavefront module."""
import sys
sys.path.append('..')
import ctypes

import pyglet
from pyglet.gl import *

import pywavefront

rotation = 0

meshes = pywavefront.Wavefront('uv_sphere.obj')

window = pyglet.window.Window()

lightfv = ctypes.c_float * 4

@window.event
def on_resize(width, height):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60., float(width)/height, 1., 100.)
    glMatrixMode(GL_MODELVIEW)
    return True

@window.event
def on_draw():
    window.clear()
    glLoadIdentity()

    glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-1.0, 1.0, 1.0, 0.0))
    glEnable(GL_LIGHT0)

    glTranslated(0, 0, -3)
    glRotatef(rotation, 0, 1, 0)
    glRotatef(-25, 1, 0, 0)
    glRotatef(45, 0, 0, 1)
    glEnable(GL_LIGHTING)

    meshes.draw()

def update(dt):
    global rotation
    rotation += 90*dt
    if rotation > 720: rotation = 0

pyglet.clock.schedule(update)

pyglet.app.run()
