from _typeshed import Incomplete

class Mesh:
    """This is a basic mesh for drawing using OpenGL. Interestingly, it does
    not contain its own vertices. These are instead drawn via materials."""
    name: Incomplete
    materials: Incomplete
    has_faces: Incomplete
    faces: Incomplete
    def __init__(self, name: Incomplete | None = None, has_faces: bool = False) -> None: ...
    def has_material(self, new_material):
        """Determine whether we already have a material of this name."""
    def add_material(self, material) -> None:
        """Add a material to the mesh, IF it's not already present."""
