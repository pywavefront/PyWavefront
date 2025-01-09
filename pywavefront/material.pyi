from _typeshed import Incomplete
from pathlib import Path as Path
from pywavefront.parser import Parser
from pywavefront.texture import Texture

logger: Incomplete

class Material:
    texture_cls = Texture
    name: Incomplete
    diffuse: Incomplete
    ambient: Incomplete
    specular: Incomplete
    emissive: Incomplete
    transparency: float
    shininess: float
    optical_density: float
    illumination_model: int
    texture: Incomplete
    texture_ambient: Incomplete
    texture_specular_color: Incomplete
    texture_specular_highlight: Incomplete
    texture_alpha: Incomplete
    texture_bump: Incomplete
    is_default: Incomplete
    vertex_format: str
    vertices: Incomplete
    gl_floats: Incomplete
    def __init__(self, name, is_default: bool = False, has_faces: bool = False) -> None:
        """
        Create a new material
        :param name: Name of the material
        :param is_default: Is this an auto created default material?
        """
    @property
    def has_normals(self): ...
    @property
    def has_uvs(self): ...
    @property
    def has_colors(self): ...
    @property
    def vertex_size(self):
        """How many float each vertex contains in the interleaved data"""
    def pad_light(self, values):
        """Accept an array of up to 4 values, and return an array of 4 values.
        If the input array is less than length 4, pad it with zeroes until it
        is length 4. Also ensure each value is a float"""
    def set_alpha(self, alpha) -> None:
        """Set alpha/last value on all four lighting attributes."""
    def set_diffuse(self, values: Incomplete | None = None) -> None: ...
    def set_ambient(self, values: Incomplete | None = None) -> None: ...
    def set_specular(self, values: Incomplete | None = None) -> None: ...
    def set_emissive(self, values: Incomplete | None = None) -> None: ...
    def set_texture(self, name, search_path) -> None: ...
    def set_texture_ambient(self, name, search_path) -> None: ...
    def set_texture_specular_color(self, name, search_path) -> None: ...
    def set_texture_specular_highlight(self, name, search_path) -> None: ...
    def set_texture_alpha(self, name, search_path) -> None: ...
    def set_texture_bump(self, name, search_path) -> None: ...
    def unset_texture(self) -> None: ...

class MaterialParser(Parser):
    """Object to parse lines of a materials definition file."""
    materials: Incomplete
    this_material: Incomplete
    collect_faces: Incomplete
    def __init__(self, file_name, strict: bool = False, encoding: str = 'utf-8', parse: bool = True, collect_faces: bool = False) -> None:
        """
        Create a new material parser
        :param file_name: file name and path of obj file to read
        :param strict: Enable strict mode
        :param encoding: Encoding to read the text files
        :param parse: Should parse be called immediately or manually called later?
        """
    def parse_newmtl(self) -> None: ...
    def parse_Kd(self) -> None: ...
    def parse_Ka(self) -> None: ...
    def parse_Ks(self) -> None: ...
    def parse_Ke(self) -> None: ...
    def parse_Ns(self) -> None: ...
    def parse_d(self) -> None:
        """Transparency"""
    def parse_Tr(self) -> None:
        """Transparency (alternative)"""
    def parse_map_Kd(self) -> None:
        """Diffuse map"""
    def parse_map_Ka(self) -> None:
        """Ambient map"""
    def parse_map_Ks(self) -> None:
        """Specular color map"""
    def parse_map_Ns(self) -> None:
        """Specular color map"""
    def parse_map_d(self) -> None:
        """Alpha map"""
    def parse_bump(self) -> None:
        """Bump map (from the spec)"""
    def parse_map_bump(self) -> None:
        """Bump map (variant)"""
    def parse_map_Bump(self) -> None:
        """Bump map (variant)"""
    def parse_Ni(self) -> None: ...
    def parse_illum(self) -> None: ...
