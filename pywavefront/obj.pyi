from _typeshed import Incomplete
from collections.abc import Generator
from pywavefront.cache import CacheLoader, CacheWriter, Meta as Meta
from pywavefront.material import MaterialParser
from pywavefront.parser import Parser

logger: Incomplete

class ObjParser(Parser):
    """This parser parses lines from .obj files."""
    material_parser_cls = MaterialParser
    cache_loader_cls = CacheLoader
    cache_writer_cls = CacheWriter
    wavefront: Incomplete
    mesh: Incomplete
    material: Incomplete
    create_materials: Incomplete
    collect_faces: Incomplete
    cache: Incomplete
    cache_loaded: Incomplete
    normals: Incomplete
    tex_coords: Incomplete
    def __init__(self, wavefront, file_name, strict: bool = False, encoding: str = 'utf-8', create_materials: bool = False, collect_faces: bool = False, parse: bool = True, cache: bool = False) -> None:
        """
        Create a new obj parser
        :param wavefront: The wavefront object
        :param file_name: file name and path of obj file to read
        :param strict: Enable strict mode
        :param encoding: Encoding to read the text files
        :param create_materials: Create materials if they don't exist
        :param cache: Cache the loaded obj files in binary format
        :param parse: Should parse be called immediately or manually called later?
        """
    def parse(self) -> None:
        """Trigger cache load or call superclass parse()"""
    def load_cache(self) -> None:
        """Loads the file using cached data"""
    def post_parse(self) -> None:
        """Called after parsing is done"""
    def parse_v(self) -> None: ...
    line: Incomplete
    values: Incomplete
    def consume_vertices(self) -> Generator[Incomplete]:
        """
        Consumes all consecutive vertices.
        NOTE: There is no guarantee this will consume all vertices since other
        statements can also occur in the vertex list
        """
    def parse_vn(self) -> None: ...
    def consume_normals(self) -> Generator[Incomplete]:
        """Consumes all consecutive texture coordinate lines"""
    def parse_vt(self) -> None: ...
    def consume_texture_coordinates(self) -> Generator[Incomplete]:
        """Consume all consecutive texture coordinates"""
    def parse_mtllib(self) -> None: ...
    def parse_usemtl(self) -> None: ...
    def parse_usemat(self) -> None: ...
    def parse_o(self) -> None: ...
    def parse_f(self) -> None: ...
    def consume_faces(self, collected_faces: Incomplete | None = None) -> Generator[Incomplete, Incomplete]:
        """
        Consume all consecutive faces

        If more than three vertices are specified, we triangulate by the following procedure:

            Let the face have n vertices in the order v_1 v_2 v_3 ... v_n, n >= 3.
            We emit the first face as usual: (v_1, v_2, v_3). For each remaining vertex v_j,
            j > 3, we emit (v_j, v_1, v_{j - 1}), e.g. (v_4, v_1, v_3), (v_5, v_1, v_4).

        In a perfect world we could consume all vertices straight forward and draw using
        GL_TRIANGLE_FAN (which exactly matches the procedure above).
        This is however rarely the case.

        * If the face is co-planar but concave, then you need to triangulate the face.
        * If the face is not-coplanar, you are screwed, because OBJ doesn't preserve enough information
          to know what tessellation was intended.

        We always triangulate to make it simple.

            :param collected_faces: A list into which all (possibly triangulated) faces will be written in the form
                                    of triples of the corresponding absolute vertex IDs. These IDs index the list
                                    self.wavefront.vertices.
                                    Specify None to prevent consuming faces (and thus saving memory usage).
        """
