from _typeshed import Incomplete

class TextureOptions:
    name: str
    blendu: str
    blendv: str
    bm: float
    boost: float
    cc: str
    clamp: str
    imfchan: str
    mm: Incomplete
    o: Incomplete
    s: Incomplete
    t: Incomplete
    texres: Incomplete
    def __init__(self) -> None:
        """Set up options with sane defaults"""

class TextureOptionsParser:
    def __init__(self, line) -> None: ...
    def parse(self): ...
    def parse_blendu(self) -> None:
        """The -blendu option turns texture blending in the horizontal direction 
        (u direction) on or off.  The default is on.
        """
    def parse_blendv(self) -> None:
        """The -blendv option turns texture blending in the vertical direction (v 
        direction) on or off.  The default is on.
        """
    def parse_bm(self) -> None:
        """The -bm option specifies a bump multiplier"""
    def parse_boost(self) -> None:
        """The -boost option increases the sharpness, or clarity, of mip-mapped 
        texture files
        """
    def parse_cc(self) -> None:
        """The -cc option turns on color correction for the texture"""
    def parse_clamp(self) -> None:
        """The -clamp option turns clamping on or off."""
    def parse_imfchan(self) -> None:
        """The -imfchan option specifies the channel used to create a scalar or 
        bump texture.
        """
    def parse_mm(self) -> None:
        """The -mm option modifies the range over which scalar or color texture 
        values may vary
        """
    def parse_o(self) -> None:
        """The -o option offsets the position of the texture map on the surface by 
        shifting the position of the map origin.
        """
    def parse_s(self) -> None:
        """The -s option scales the size of the texture pattern on the textured 
        surface by expanding or shrinking the pattern
        """
    def parse_t(self) -> None:
        """The -t option turns on turbulence for textures."""
    def parse_texres(self) -> None:
        """The -texres option specifies the resolution of texture created when an 
        image is used.
        """

class Texture:
    image: Incomplete
    def __init__(self, name, search_path) -> None:
        """Create a texture.

        Args:
            name (str): The texture name possibly with path and options as it appear in the material
            search_path (str): Absolute or relative path the texture might be located.
        """
    @property
    def name(self):
        """str: The texture path as it appears in the material"""
    @name.setter
    def name(self, value) -> None: ...
    @property
    def options(self) -> TextureOptions:
        """TextureOptions: Options for this texture"""
    def find(self, path: Incomplete | None = None):
        """Find the texture in the configured search path
        By default a search will be done in the same directory as
        the obj file including all subdirectories if ``path`` does not exist.

        Args:
            path: Override the search path
        Raises:
            FileNotFoundError if not found
        """
    @property
    def file_name(self):
        """str: Obtains the file name of the texture.
        Sometimes materials contains a relative or absolute path
        to textures, something that often doesn't reflect the
        textures real location.
        """
    @property
    def path(self):
        """str: search_path + name"""
    @path.setter
    def path(self, value) -> None: ...
    @property
    def image_name(self):
        """Wrap the old property name to not break compatibility.
        The value will always be the texture path as it appears in the material.
        """
    @image_name.setter
    def image_name(self, value) -> None:
        """Wrap the old property name to not break compatibility"""
    def exists(self):
        """bool: Does the texture exist"""
