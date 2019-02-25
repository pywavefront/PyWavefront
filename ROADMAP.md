
# PyWavefront 2.0

## Introduction

PyWavefront is used by projects and people from both data science and pure 3D
rendering. Providing visualisation capabilities also seems to be important for
a lot of users. There are ties to [pyglet](https://bitbucket.org/pyglet/pyglet/wiki/Home)
we probably should not break.

Currently the project mainly has 3D rendering in mind. We see that in the parser
were interlaved vertex data is genereted on the fly. This is not always what
users want and will need improvements. Collecting face data was also added
fairly recently but is limited to trinagles to make it consistent with the
rest of the library.

The plan is to revamp the project structure and making the parse result a lot more flexible supporting triangles and quads + other optimization. The goal is to make the library easier to use for data science as well as 3d rendering. Parsing should only
collect the actual data. We then provide methods for obtaining the data in
various ways after the parse is done.


## Improved Visualization

To provide a modern cross-platform visualization system moving to 
[ModernGL](https://github.com/cprogrammer1994/ModernGL) is probably
the way to go using PyQt5 as the default rendering window.

**It's still important to also keep a pyglet option as a lot of
users would expect this to be present.**

We can simply brush up the old pyglet visualitzation module and
migrate that to using shaders when Pyglet 2.x is out.

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
