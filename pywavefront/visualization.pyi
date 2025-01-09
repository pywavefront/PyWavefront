from pyglet.gl import *
from _typeshed import Incomplete
from pywavefront.mesh import Mesh as Mesh

def same(v): ...

VERTEX_FORMATS: Incomplete

def draw(instance, lighting_enabled: bool = True, textures_enabled: bool = True) -> None:
    """Generic draw function"""
def draw_materials(materials, lighting_enabled: bool = True, textures_enabled: bool = True) -> None:
    """Draw a dict of meshes"""
def draw_material(material, face=..., lighting_enabled: bool = True, textures_enabled: bool = True) -> None:
    """Draw a single material"""
def gl_light(lighting):
    """Return a GLfloat with length 4, containing the 4 lighting values."""
def bind_texture(texture) -> None:
    """Draw a single texture"""
def load_image(name):
    """Load an image"""
def verify_dimensions(image) -> None: ...
def verify(image, dimension) -> None: ...
