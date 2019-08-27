# Change Log

Release history on Github: https://github.com/pywavefront/PyWavefront/releases

## 1.2.0

* Pywavefront is now using `pathlib` internally. `Path` instances can also
  be passed to all parsers.
* Bugfix: Texture paths in materials should no longer be mangled when
  containing spaces or special characters. It should always be read
  exactly as it appears in the file.
* Texture: `file_name` property added as a more robust way to get
  the texture file name without path. This should even work for
  hardcoded windows path on Linux and OS X.
* Texture: Added `find` method searching for the exact texture name in a directory
  and all subdirectories. By default it will search from the obj file's location.
* Visualization: `draw` methods now supports `lighting_enabled` and `textures_enabled`
  making the user able to toggle on/off lighting and texturing.

## 1.1.0

* Fixed an incompatibility issue related to image loading in pyglet 1.4.x
* Texture instances now store the texture name as they apprear in the material
  and an optional path parameter that represents the absolute path to the
  texture.
* Removed dead code related related to python 2/3 compatibility

## 1.0.5

* Visualization module should enable depth testing by default.
  This is what most people need.

## 1.0.4

* Faces with undefined texture coordinates will
  fall back to uv index 0

## 1.0.3

* Fix vertex format exceptions - PR #86

## 1.0.2

* Fix two parsing IndexErrors - PR #84

## 1.0.1

* Release only for Python3, not universal - Fixes #79

## 1.0.0

* Use Python 3.4 on CI server - PR #78
* Switch to Python 3.4+ - PR #77
* Fix support for earlier py3 versions, which do not support json as bytes - PR #76
* Add option to retain face data - PR #74

## 0.4.2

* Add Python 3.7 support - PR #72
* Add missing material properties - PR #70
* Tweak README - PR #68

## 0.4.1

* Add Python 3 - PR #65

## 0.4.0
* Add binary cache - PR #63
* Fix handling of negative indices - PR #62
* Set up logger - PR #60
* Allow textures to load from anywhere - PR #59

## 0.3.2

* Fix README - PR #55
* Allow users to override material parser - PR #54
* Allow parser to create missing materials - PR #52
* Fix pypi markdown, tweak README - PR #51

## 0.3.1

* Revamp README - PR #48
* Fix various bugs - PR #47
* Cap shininess in visualization - PR #46
* Support different vertex formats + example - PR #43
* Detect vertex format, vertex color, and tests - PR #42

## 0.3.0

* Run all parser tests for gzip file - PR #40
* Revamp parser to prepare to support different vertex formats - PR #38
* Make dir available as instance attribute + tests - PR #33
* Use setuptools - PR #31

## 0.2.0

* Make Pyglet an optional dependency - PR #30
* Close file descriptor when no longer needed - PR #29
* Specify the full path for the test files. Remove Pyglet dependency on unit tests - PR #28
* Use the correct accented "e" character- PR #27
* Add basic circleci configuration

## 0.1.7

* Handle any unimplemented flag and carry on with a warning - PR #21
* Add support to object-less obj file - PR #23

## 0.1.6

* Import .obj without material file - PR #16

## 0.1.5

* Support transparency - PR #15

## 0.1.4

* Include MANIFEST file - PR #12

## 0.1.3

* Replace Pyglet resource with native open() - PR #7
* Remove UTF-8 encoding/decoding - PR #9
* Fix issues with parsing resource files - PR #9

## 0.1.2

* Update syntax to Python 3 - PR #3
* Add support for opening .obj files in other directories - PR #5
* Conform to PEP 8 - PR #5
* Add support for relative imports - PR #5

## 0.1.1

* Add material setters.
* Add lighting in example.

## 0.1

* Initial release.
