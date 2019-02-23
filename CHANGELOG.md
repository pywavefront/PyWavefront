Change Log

Release history on Github: https://github.com/pywavefront/PyWavefront/releases

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
