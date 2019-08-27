# ----------------------------------------------------------------------------
# PyWavefront
# Copyright (c) 2013 Kurt Yoder
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of PyWavefront nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------
import pywavefront
from pathlib import Path, PureWindowsPath
import re


class Texture:
    def __init__(self, name, search_path):
        """Create a texture.

        Args:
            name (str): The texture possibly with path as it appear in the material
            search_path (str): Absolute or relative path the texture might be located.
        """
        self._name = name
        self._search_path = Path(search_path)
        self._path = Path(search_path, name)

        # Unsed externally by visualization
        self.image = None

    @property
    def name(self):
        """str: The texture path as it appears in the material"""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def find(self, path=None):
        """Find the texture in the configured search path
        By default a search will be done in the same directory as
        the obj file including all subdirectories if ``path`` does not exist.

        Args:
            path: Override the search path
        Raises:
            FileNotFoundError if not found
        """
        if self.exists():
            return self.path

        search_path = path or self._search_path
        locations = Path(search_path).glob('**/{}'.format(self.file_name))
        # Attempt to look up the first entry of the generator
        try:
            first = next(locations)
        except StopIteration:
            raise FileNotFoundError("Cannot locate texture `{}` in search path: {}".format(
                self._name, search_path))

        return str(first)

    @property
    def file_name(self):
        """str: Obtains the file name of the texture.
        Sometimes materials contains a relative or absolute path
        to textures, something that often doesn't reflect the
        textures real location.
        """
        if ':' in self._name or '\\' in self._name:
            return PureWindowsPath(self._name).name

        return Path(self._name).name

    @property
    def path(self):
        """str: search_path + name"""
        return str(self._path)

    @path.setter
    def path(self, value):
        self._path = Path(value)

    @property
    def image_name(self):
        """Wrap the old property name to not break compatibility.
        The value will always be the texture path as it appears in the material.
        """
        return self._name

    @image_name.setter
    def image_name(self, value):
        """Wrap the old property name to not break compatibility"""
        self._name = value

    def exists(self):
        """bool: Does the texture exist"""
        return self._path.exists()
