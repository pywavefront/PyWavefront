from _typeshed import Incomplete
from pywavefront.material import MaterialParser

logger: Incomplete

def cache_name(path):
    """Generate the name of the binary cache file"""
def meta_name(path):
    """Generate the name of the meta file"""

class CacheLoader:
    material_parser_cls = MaterialParser
    wavefront: Incomplete
    file_name: Incomplete
    path: Incomplete
    encoding: Incomplete
    strict: Incomplete
    dir: Incomplete
    meta: Incomplete
    def __init__(self, file_name, wavefront, strict: bool = False, create_materials: bool = False, encoding: str = 'utf-8', parse: bool = True, **kwargs) -> None: ...
    def parse(self): ...
    def load_vertex_buffer(self, fd, material, length) -> None:
        """
        Load vertex data from file. Can be overriden to reduce data copy

        :param fd: file object
        :param material: The material these vertices belong to
        :param length: Byte length of the vertex data
        """

class CacheWriter:
    file_name: Incomplete
    wavefront: Incomplete
    meta: Incomplete
    def __init__(self, file_name, wavefront) -> None: ...
    def write(self) -> None: ...

class Meta:
    """
    Metadata for binary obj cache files
    """
    format_version: str
    def __init__(self, **kwargs) -> None: ...
    def add_vertex_buffer(self, material, vertex_format, byte_offset, byte_length) -> None:
        """Add a vertex buffer"""
    @classmethod
    def from_file(cls, path): ...
    def write(self, path) -> None:
        """Save the metadata as json"""
    @property
    def version(self): ...
    @property
    def created_at(self): ...
    @property
    def vertex_buffers(self): ...
    @property
    def mtllibs(self): ...
    @mtllibs.setter
    def mtllibs(self, value) -> None: ...
