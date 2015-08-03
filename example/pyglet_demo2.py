#!/usr/bin/env python
"""This script shows another example of using the PyWavefront module."""
# This example was created by intrepid94
import sys
sys.path.append('..')
import ctypes

import pyglet
from pyglet.gl import *

from pywavefront import Wavefront

rotation = 0

meshes = Wavefront('earth.obj')

window = pyglet.window.Window(1024, 720, caption = 'Demo', resizable = True)

lightfv = ctypes.c_float * 4
label = pyglet.text.Label('Hello, world', font_name = 'Times New Roman', font_size = 12, x = 800, y = 700, anchor_x = 'center', anchor_y = 'center')
@window.event
def on_resize(width, height):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40.0, float(width)/height, 1, 100.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
    return True

@window.event
def on_draw():
    window.clear()
    glLoadIdentity()
    glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, lightfv(0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightfv(0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_MODELVIEW)
    # glTranslated(0, 4, -8)
 #    glRotatef(90, 0, 1, 0)
 #    glRotatef(-60, 0, 0, 1)
   # Rotations for sphere on axis - useful
    glTranslated(0, .8, -20)
    glRotatef(-66.5, 0, 0, 1)
    glRotatef(rotation, 1, 0, 0)
    glRotatef(90, 0, 0, 1)
    glRotatef(0, 0, 1, 0)
    meshes.draw()
def update(dt):
    global rotation
    rotation += 45 * dt
    if rotation > 720: 
       rotation = 0

pyglet.clock.schedule(update)

pyglet.app.run()
