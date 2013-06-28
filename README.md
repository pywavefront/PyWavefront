PyWavefront
===========

This python module allows you to convert Wavefront 3D object files
(`something.obj` and `something.mtl`) into Python objects. Currently
Pyglet is required to render and display these objects.

Requirements
------------

* Pyglet

Usage
-----

### From Python

    import pywavefront
    meshes = pywavefront.Wavefront('something.obj')
    meshes.draw()

### Example Script

A pyglet example script with included `.obj` and `.mtl` files is
included in the `example` directory. To run it, change to the `example`
directory and run `./pyglet.py`.

Installation
------------

Tests
-----

License
-------
