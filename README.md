PyWavefront
===========

This python module allows you to read Wavefront 3D object files
(`something.obj` and `something.mtl`) and use them as Python objects.
Currently Pyglet is required to render and display these objects.

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
directory and run `./pyglet_demo.py`.

Installation
------------

Tests
-----

All tests can be found in the `test` directory. To run the tests:

* Install nose: `pip install nose`
* Change to the top-level directory, e.g. `PyWavefront`, the directory that contains this `README` file.
* Run `nosetests`

License
-------
