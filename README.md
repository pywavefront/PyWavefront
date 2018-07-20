[![pypi](https://img.shields.io/pypi/v/PyWavefront.svg)](https://pypi.org/project/PyWavefront/)
[![CircleCI](https://circleci.com/gh/greenmoss/PyWavefront.svg?style=svg)](https://circleci.com/gh/greenmoss/PyWavefront)

PyWavefront
===========

PyWavefront reads Wavefront 3D object files (`something.obj` and `something.mtl`)
and generates interleaved vertex data for each material ready for rendering.
Python 2.7.x or 3.6+ is supported. A simple (optional) visualization module is also
provided for rendering the object(s). The interleaved data can also be used by
more modern renderers thought VBOs or VAOs.

Currently the most commonly used features in [the defined specification](https://en.wikipedia.org/wiki/Wavefront_.obj_file) has
been implemented. Positions, texture coordinates, normals, vertex color and material parsing.
We currently don't support parameter space vertices, line elements or smoothing groups.
Create an issue or pull request on github if needed features are missing.

The package is on pypi or can be cloned on [github](https://github.com/greenmoss/PyWavefront).

```
pip install PyWavefront
```

## Usage

Basic example loading an obj file:

```python
import pywavefront
scene = pywavefront.Wavefront('something.obj')
```

A more complex example

* `strict` (Default: `False`) will raise an exception if unsupported features are found in the obj or mtl file
* `encoding` (Default: `utf-8`) of the obj and mtl file(s)
* `create_materials` (Default: `False`) will create materials if mtl file is missing or obj file references non-existing materials
* `parse` (Default: `True`) decides if parsing should start immediately.
* `cache` (Default: `False`) writes the parsed geometry to a binary file    for faster loading in the future

```python
import pywavefront
scene = pywavefront.Wavefront('something.obj', strict=True, encoding="iso-8859-1", parse=False)
scene.parse()  # Explicit call to parse() needed when parse=False

# Iterate vertex data collected in each material
for name, material in scene.materials.items():
    # Contains the vertex format (string) such as "T2F_N3F_V3F"
    # T2F, C3F, N3F and V3F may appear in this string
    material.vertex_format
    # Contains the vertex list of floats in the format described above
    material.vertices
    # Material properties
    material.diffuse
    material.ambient
    material.texture
    # ..
```

## Binary Cache

When ``cache=True`` the interleaved vertex data is written
as floats to a ``.bin`` file after the file is loaded. A json
file is also generated describing the contents of the binary file.
The binary file will be loaded the next time we attept to load
the obj file reducing the loading time greatly.

Tests have shown loading time reduction by 10x to 30x.

Loading ``myfile.obj`` will generate the following files in the
same directory.

```
myfile.obj.bin
myfile.obj.json
```

Json file example:

```json
{
  "created_at": "2018-07-16T14:28:43.451336",
  "version": "0.1",
  "materials": [
    "lost_empire.mtl"
  ],
  "vertex_buffers": [
    {
      "material": "Stone",
      "vertex_format": "T2F_N3F_V3F",
      "byte_offset": 0,
      "byte_length": 5637888
    },
    {
      "material": "Grass",
      "vertex_format": "T2F_N3F_V3F",
      "byte_offset": 5637888,
      "byte_length": 6494208
    }
  ]
}
```

These files will not be recreated until you delete them.
The bin file is also compessed with gzip to greatly reduce size.

## Visualization

[Pyglet](http://www.pyglet.org/) is required to use the visualization module.
```
pip install pyglet
```

Example:

```python
import pywavefront
from pywavefront import visualization

[create a window and set up your OpenGl context]
obj = pywavefront.Wavefront('something.obj')

[inside your drawing loop]
visualization.draw(obj)
```

## Logging

The default log level is `ERROR`. This is configurable including overriding the formatter.

```python
import logging
import pywavefront

pywavefront.configure_logging(
    logging.DEBUG,
    formatter=logging.Formatter('%(name)s-%(levelname)s: %(message)s')
)
```

### Example Scripts

The `example` directory contains some basic examples using the `visualization` module

* `pyglet_demo.py` : Simple textured globe
* `pyglet_demo2.py` : Higher resolution textured globe
* `pyglet_demo_boxes.py` : Boxes demonstrating supported vertex formats of the visualization module

### Generating a Wavefront file with Blender

The following presumes you are using [Blender](http://www.blender.org/) to generate your mesh:

* Using Blender, create a mesh with a UV-mapped texture. The UV-mapping is important! If it is working properly, you will see the texture applied within Blender's 3d view.
* Export the mesh from Blender using the Wavefront format, including normals.
* Reference your `*.obj` file as in the pywavefront example above.

## Tests

All tests can be found in the `test` directory. To run the tests:

* Install nose: `pip install nose`
* Change to the top-level directory, e.g. `PyWavefront`, the directory that contains this `README` file.
* Run `nosetests`

## Community

Slack: [channel](https://pywavefront.slack.com/). [Email the admins](mailto:pywavefront+slack@gmail.com?subject=Please%20send%20me%20an%20invitation%20to%20the%20PyWavefront%20Slack%20channel&body=Thanks!) 
to request an invitation. Ensure you leave the subject line intact!

## Contributors

* Daniel Coelho
* dav92lee
* Einar Forselv
* Jerek Shoemaker
* Kurt Yoder
* Marxlp
* Patrik Huber
* Sérgio Agostinho
* Zohar Jackson

License
-------

PyWavefront is BSD-licensed; see file `LICENSE`.
