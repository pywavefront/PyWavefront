PyWavefront
===========

This python module allows you to read Wavefront 3D object files
(`something.obj` and `something.mtl`) and use them as Python objects.
If you optionally want to render and display these objects, Pyglet is required.

Currently, only a subset of [the defined
specification](https://en.wikipedia.org/wiki/Wavefront_.obj_file) has
been implemented.

Optional Dependencies
------------

* [Pyglet](http://www.pyglet.org/)

Usage
-----

### From Python

**Basic**

```python
import pywavefront
meshes = pywavefront.Wavefront('something.obj')
```

**Visualization**

```python
import pywavefront

[create a window and set up your OpenGl context]
meshes = pywavefront.Wavefront('something.obj')

[inside your drawing loop]
meshes.draw()
```

### Example Script

There are two pyglet example scripts with included `.obj` and `.mtl` files in the `example` directory. To run them, change to the `example`
directory and run either `./pyglet_demo.py` or `.pyglet_demo2.py`. Pyglet is required for these.

### Generating a Wavefront file with Blender

The following presumes you are using [Blender](http://www.blender.org/) to generate your mesh:

* Using Blender, create a mesh with a UV-mapped texture. The UV-mapping is important! If it is working properly, you will see the texture applied within Blender's 3d view.
* Export the mesh from Blender using the Wavefront format, including normals.
* Reference your `*.obj` file as in the pywavefront example above.

Installation
------------

### Source distribution

Assuming you are in the top-level PyWavefront directory:

    python setup.py install

### Pip

    pip install PyWavefront

Tests
-----

All tests can be found in the `test` directory. To run the tests:

* Install nose: `pip install nose`
* Change to the top-level directory, e.g. `PyWavefront`, the directory that contains this `README` file.
* Run `nosetests`

Contributors
-------

* Daniel Coelho
* dav92lee
* Jerek Shoemaker
* Kurt Yoder
* Marxlp
* Patrik Huber
* Sérgio Agostinho
* Zohar Jackson

License
-------

PyWavefront is BSD-licensed; see file `LICENSE`.
