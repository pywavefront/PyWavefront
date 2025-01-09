from _typeshed import Incomplete
from pywavefront import ObjParser

logger: Incomplete

class Wavefront:
    parser_cls = ObjParser
    file_name: Incomplete
    mtllibs: Incomplete
    materials: Incomplete
    meshes: Incomplete
    vertices: Incomplete
    mesh_list: Incomplete
    parser: Incomplete
    def __init__(self, file_name, strict: bool = False, encoding: str = 'utf-8', create_materials: bool = False, collect_faces: bool = False, parse: bool = True, cache: bool = False) -> None:
        """
        Create a Wavefront instance
        :param file_name: file name and path of obj file to read
        :param strict: Enable strict mode
        :param encoding: What text encoding the parser should use
        :param create_materials: Create materials if they don't exist
        :param parse: Should parse be called immediately or manually called later?
        """
    def parse(self) -> None:
        """Manually call the parser. This is used when parse=False"""
    def add_mesh(self, the_mesh) -> None: ...
