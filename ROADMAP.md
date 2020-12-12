
# PyWavefront 2.0

## Introduction

PyWavefront is used by projects and people from both data science and pure 3D
rendering. Providing visualisation capabilities also seems to be important for
a lot of users. There are ties to [pyglet](https://github.com/pyglet/pyglet)
we probably should not break.

Currently the project mainly has 3D rendering in mind. We see that in the parser
were interlaved vertex data is genereted on the fly. This is not always what
users want and will need improvements. Collecting face data was also added
fairly recently but is limited to trinagles to make it consistent with the
rest of the library.

The plan is to revamp the project structure and making the parse result a lot more flexible supporting triangles and quads + other optimization. The goal is to make the library easier to use for data science as well as 3d rendering. Parsing should only
collect the actual data. We then provide methods for obtaining the data in
various ways after the parse is done.

Better resolve and locate textures referenced in materials. Right
now the `Texture` class is a bit of a mess because of almost a
decade of not breaking compatibility.

## Documentation

Write proper docs using either readthedocs or github pages.
A `docs` branch was started a while ago and we should revive that.


## Improved Visualization

Pyglet has changed a lot lately with then 1.4 release and a 2.0
release with shaders is in the works. We should definitley
upgrade the viewer to support basic shaders even if we only
stick with GL2.1.

Possibly also provide a 3.3+ viewer with pyglet. A ModernGL
alternative could also be nice.

Support proper window resizing and camera so people can inspect
their models. Maybe also expose things like fullscreen mode.

We must not forget this library is popular because of the simple
viewing capabilities.

## Introduce pywavefront Command

Bring PyWavefront to the command line making common operations easily
accessible.

```bash
# Renders the obj file
pywavefront show test.obj

# Cache management
pywavefront gen_cache test.obj
pywavefront del_cache test.obj

# .. possibly other commands
```

## Memory Management

TLDR; Use `numpy` to store internal data using 6 times less memory.

We are currently collecting and storing indices and postions using native
python types.

```py
>> import sys
>> data = [x for x in range(1000000)]
>> f"Array size: {(len(data) * sys.getsizeof(int())) // 1024 // 1024} MB")
Array size: 22.8876953125 MB
>> f"sizeof int: {sys.getsizeof(int())} bytes"
sizeof int: 24 bytes
>> f"sizeof float: {sys.getsizeof(float())} bytes"
sizeof float: 24 bytes
```

As we can see an `int` and `float` actually takes 24 bytes in python.
This is 6 times more than necessary

With `numpy` we can solve this entirely

```py
import numpy as np
data = np.arange(1_000_000)
f"Item size: {data.itemsize}"
Item size: 4
f"Array size: {len(data) * data.itemsize / 1024 / 1024} MB"
Array size: 3.814697265625 MB
```

An advantage is also that we can reshape the array without
allocating new memory.
